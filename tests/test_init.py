"""Test for the EMSC CSEM Earthquakes feed."""
import datetime
import unittest
from unittest import mock

from georss_client import UPDATE_OK
from georss_client.exceptions import GeoRssException
from tests import load_fixture
from georss_emsc_csem_earthquakes_client import EMSCEarthquakesFeed

HOME_COORDINATES = (46.1, 14.2)

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

        feed = EMSCEarthquakesFeed(HOME_COORDINATES)
        assert repr(feed) == "<EMSCEarthquakesFeed(" \
                             "home=(46.1, 14.2), url=https://www.emsc-csem.org/service/rss/rss.php?typ=emsc&min_lat=10&min_long=-30&max_long=65, " \
                             "filter_radius=None, filter_min_magnitude=None)>"
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 2

        feed_entry = entries[0]
        assert feed_entry.title == "ML 2.2  PYRENEES"
        assert feed_entry.external_id == "https://www.emsc-csem.org/Earthquake/earthquake.php?id=934374"
        assert feed_entry.coordinates == (42.90, 0.20)
        #self.assertAlmostEqual(feed_entry.distance_to_home, ???, 1)
        assert feed_entry.published \
            == datetime.datetime(2020, 12, 30, 21, 35,
                                 tzinfo=datetime.timezone.utc)
        assert feed_entry.magnitude == 2.2
        #assert feed_entry.attribution == None
        assert repr(feed_entry) == "<EMSCEarthquakesFeedEntry(id=https://www.emsc-csem.org/Earthquake/earthquake.php?id=934374, " \
                                   "title=ML 2.2  PYRENEES, link=https://www.emsc-csem.org/Earthquake/earthquake.php?id=934374, " \
                                    "geometry=<Point(latitude=42.9, longitude=0.2)>, time=2020-12-30 21:14:43 UTC, depth=2, magnitude=2.2)>"

        feed_entry = entries[1]
        assert feed_entry.title == "ML 2.8  CRETE, GREECE"
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

        feed = EMSCEarthquakesFeed(HOME_COORDINATES, filter_minimum_magnitude=2.5)
        assert repr(feed) == "<EMSCEarthquakesFeed(" \
                             "home=(46.1, 14.2), url=https://www.emsc-csem.org/service/rss/rss.php?typ=emsc&min_lat=10&min_long=-30&max_long=65, " \
                             "filter_radius=None, filter_min_magnitude=2.5)>"
        status, entries = feed.update()
        assert status == UPDATE_OK
        self.assertIsNotNone(entries)
        assert len(entries) == 1
