import re
from eqinfoscraper.data_processor import get_earthquake_entries, get_stats
from eqinfoscraper.data_processor import display
from eqinfoscraper.constants import VALID_URL_FORMATS


class EarthquakeList:
    def __init__(self, URL, cutoff_date=None):
        self._source = self._identify_url_source(URL)
        self._eq_list = get_earthquake_entries(URL, self._source, cutoff_date)
        self._eq_stats = get_stats(self._source, self._eq_list)

    def __iter__(self):
        return iter(self._eq_list)

    def get_raw_eq_list(self):
        return self._eq_list

    def get_raw_eq_stats(self):
        return self._eq_stats

    def display_overview(self):
        if self._source == "PHIVOLCS":
            display.phivolcs.display_overview(self._eq_stats)
        if self._source == "JMA":
            display.jma.display_overview(self._eq_stats)

    def display_all_entries(self):
        if self._source == "PHIVOLCS":
            display.phivolcs.display_all_entries(self._eq_list)
        if self._source == "JMA":
            display.jma.display_all_entries(self._eq_list)

    def _identify_url_source(self, URL):
        for pattern in VALID_URL_FORMATS["JMA"]:
            if re.match(pattern, URL):
                return "JMA"

        for pattern in VALID_URL_FORMATS["PHIVOLCS"]:
            if re.match(pattern, URL):
                return "PHIVOLCS"
