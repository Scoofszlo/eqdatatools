from abc import ABC, abstractmethod
from datetime import datetime
from eqdatatools.constants import VALID_DATE_FORMATS


class DataScraper(ABC):
    def __new__(cls, url, start_date):
        instance = super(DataScraper, cls).__new__(cls)
        instance.__init__(url, start_date)

        return instance.eq_list

    def __init__(self, url, start_date):
        self.eq_list = []
        self._scrape_data(url, start_date)

    def __iter__(self):
        return iter(self.eq_list)

    def _is_date_before_start_date(self, retrieve_date, start_date):
        """
        This ensures no earthquake entries will be extracted when its
        date is before the specified start date. For example, if the start date is
        January 10, 2024 at 11:35 pm. Any earthquake entries before that
        date and time will not be processed.
        """

        start_date = datetime.strptime(start_date, VALID_DATE_FORMATS["DEFAULT"][0])

        if retrieve_date < start_date:
            return True

    @abstractmethod
    def _scrape_data(self, url, cutoff_date):
        pass

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
