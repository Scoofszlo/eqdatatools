from abc import ABC, abstractmethod
from eqinfoscraper.exceptions import InvalidURLError


class BaseScraper(ABC):
    def __new__(cls, url, cutoff_date=None):
        instance = super(BaseScraper, cls).__new__(cls)
        instance.__init__(url, cutoff_date)

        return instance.eq_list

    def __init__(self, url, cutoff_date=None):
        self.eq_list = []
        self._scrape_data(url, cutoff_date)

    def __iter__(self):
        return iter(self.eq_list)

    def _scrape_data(self, url, cutoff_date):
        if not self._is_valid_url(url):
            raise InvalidURLError(url)

        webpage = self._get_html_content_as_soup(url)

        eq_entries_table = self._get_eq_data_table(webpage)
        if not eq_entries_table:
            return None

        for entry in eq_entries_table:
            data = self._extract_data(entry, cutoff_date)
            if data:
                self.eq_list.append(data)

    @abstractmethod
    def _is_valid_url(self, url):
        """
        Checks the URL if it is one of the valid URLs supported for extraction
        of data.
        """
        pass

    @abstractmethod
    def _extract_data(self, entry, cutoff_date):
        pass

    @abstractmethod
    def _is_before_cutoff_date(self, retrieve_date, cutoff_date):
        pass

    @abstractmethod
    def _get_date(self, entry):
        pass

    @abstractmethod
    def _get_coordinates(self, entry):
        pass

    @abstractmethod
    def _get_depth(self, entry):
        pass

    @abstractmethod
    def _get_magnitude(self, entry):
        pass

    @abstractmethod
    def _get_event_details_url(self, entry):
        pass

    @abstractmethod
    def _get_location(self, entry):
        pass
