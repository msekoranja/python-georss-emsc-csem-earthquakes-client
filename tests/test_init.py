"""Test for the EMSC CSEM Earthquakes feed."""
import datetime
import unittest
from unittest import mock

from georss_client import UPDATE_OK
from georss_client.exceptions import GeoRssException
from tests import load_fixture

HOME_COORDINATES = (46, 14)


class TestEMSCEarthquakesFeed(unittest.TestCase):
    """Test the EMSC CSEM Canada Earthquakes feed."""

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok_en(self, mock_session, mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = \
            load_fixture('emsc_csem_earthquakes.xml')

        feed = NaturalResourcesCanadaEarthquakesFeed(HOME_COORDINATES)
        assert repr(feed) == "<NaturalResourcesCanadaEarthquakesFeed(" \
                             "home=(49.25, -123.1), url=http://www." \
                             "earthquakescanada.nrcan.gc.ca/index-en.php?" \
                             "tpl_region=canada&tpl_output=rss, " \
                             "radius=None, magnitude=None)>"
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 2

        feed_entry = entries[0]
        assert feed_entry.title == "Title 1"
        assert feed_entry.external_id == "1234"
        assert feed_entry.coordinates == (44.11, -66.23)
        self.assertAlmostEqual(feed_entry.distance_to_home, 4272.4, 1)
        assert feed_entry.published \
            == datetime.datetime(2018, 9, 29, 8, 30,
                                 tzinfo=datetime.timezone.utc)
        assert feed_entry.category == "Category 1"
        assert feed_entry.magnitude == 4.5
        assert feed_entry.attribution == "Natural Resources Canada"
        assert repr(feed_entry) == "<NaturalResourcesCanadaEarthquakes" \
                                   "FeedEntry(id=1234)>"

        feed_entry = entries[1]
        assert feed_entry.title == "Title 2"
        self.assertIsNone(feed_entry.published)

    @mock.patch("requests.Request")
    @mock.patch("requests.Session")
    def test_update_ok_en_with_magnitude(self, mock_session, mock_request):
        """Test updating feed is ok."""
        mock_session.return_value.__enter__.return_value.send\
            .return_value.ok = True
        mock_session.return_value.__enter__.return_value.send\
            .return_value.text = \
            load_fixture('emsc_csem_earthquakes.xml')

        feed = NaturalResourcesCanadaEarthquakesFeed(
            HOME_COORDINATES, filter_minimum_magnitude=4.0)
        assert repr(feed) == "<NaturalResourcesCanadaEarthquakesFeed(" \
                             "home=(49.25, -123.1), url=http://www." \
                             "earthquakescanada.nrcan.gc.ca/index-en.php?" \
                             "tpl_region=canada&tpl_output=rss, " \
                             "radius=None, magnitude=4.0)>"
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 1

        feed_entry = entries[0]
        assert feed_entry.title == "Title 1"
        assert feed_entry.external_id == "1234"
