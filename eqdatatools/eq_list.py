import re
from eqdatatools.data_processor import (
    get_earthquake_entries,
    get_stats,
    display_overview,
    display_all_entries
)
from eqdatatools.constants import VALID_URL_FORMATS


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
        display_overview(self._source, self._eq_list, self._eq_stats)

    def display_all_entries(self):
        display_all_entries(self._source, self._eq_list, self._eq_stats)

    def _identify_url_source(self, URL):
        for pattern in VALID_URL_FORMATS["JMA"]:
            if re.match(pattern, URL):
                return "JMA"

        for pattern in VALID_URL_FORMATS["PHIVOLCS"]:
            if re.match(pattern, URL):
                return "PHIVOLCS"
