from abc import ABC, abstractmethod
import re
from typing import Dict, List, Any, Iterator
from eqdatatools import scraper
from eqdatatools.data_processor import display
from eqdatatools.data_processor import stats
from eqdatatools.constants import VALID_URL_FORMATS
from eqdatatools.exceptions import InvalidURLError


class EarthquakeList:
    def __new__(cls, url: str, start_date: str = None):
        url_source = cls._identify_url_source(url)

        if url_source == "JMA":
            return JMAEarthquakeList(url, start_date)
        elif url_source == "PHIVOLCS":
            return PHIVOLCSEarthquakeList(url, start_date)
        else:
            raise InvalidURLError(url)

    @staticmethod
    def _identify_url_source(url: str) -> str:
        for pattern in VALID_URL_FORMATS["JMA"]:
            if re.match(pattern, url):
                return "JMA"

        for pattern in VALID_URL_FORMATS["PHIVOLCS"]:
            if re.match(pattern, url):
                return "PHIVOLCS"

        raise InvalidURLError(url)


class BaseEarthquakeList(ABC):
    def __init__(self, url: str, start_date: str) -> None:
        self._eq_list = self._get_earthquake_entries(url, start_date)
        self._eq_stats = self._get_stats()

    def __iter__(self) -> Iterator[Any]:
        return iter(self._eq_list)

    def get_raw_eq_list(self) -> List[Dict[str, Any]]:
        return self._eq_list

    def get_raw_eq_stats(self) -> Dict[str, Any]:
        return self._eq_stats

    @abstractmethod
    def display_overview(self) -> None:
        pass

    @abstractmethod
    def display_all_entries(self) -> None:
        pass

    @abstractmethod
    def _get_earthquake_entries(self, url: str, start_date: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def _get_stats(self) -> Dict[str, Any]:
        pass


class PHIVOLCSEarthquakeList(BaseEarthquakeList):
    def __init__(self, url: str, start_date: str):
        super().__init__(url, start_date)
        self.eq_display = display.PHIVOLCSDisplayEQData(self._eq_list, self._eq_stats)

    def display_overview(self) -> None:
        self.eq_display.display_overview()

    def display_all_entries(self) -> None:
        self.eq_display.display_all_entries()

    def _get_earthquake_entries(self, url: str, start_date: str) -> List[Dict[str, Any]]:
        eq_list = scraper.phivolcs.scrape_data(url, start_date)
        return eq_list

    def _get_stats(self) -> Dict[str, Any]:
        eq_stats = stats.phivolcs.get_stats(self._eq_list)
        return eq_stats


class JMAEarthquakeList(BaseEarthquakeList):
    def __init__(self, url: str, start_date: str):
        super().__init__(url, start_date)
        self.eq_display = display.JMADisplayEQData(self._eq_list, self._eq_stats)

    def display_overview(self) -> None:
        self.eq_display.display_overview()

    def display_all_entries(self) -> None:
        self.eq_display.display_all_entries()

    def _get_earthquake_entries(self, url: str, start_date: str) -> List[Dict[str, Any]]:
        eq_list = scraper.jma.scrape_data(url, start_date)
        return eq_list

    def _get_stats(self) -> Dict[str, Any]:
        eq_stats = stats.jma.get_stats(self._eq_list)
        return eq_stats
