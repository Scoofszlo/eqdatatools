import re
import requests
from bs4 import BeautifulSoup
from eqdatatools.constants import (
    PHIVOLCS_CA_CERT_PATH,
    DATE_REGEX_PATTERN,
    NON_PRINTABLE_CHAR_PATTERN
)
from eqdatatools.scraper._utils import convert_to_datetime_obj
from ._base import DataScraper


class PHIVOLCSScraper(DataScraper):
    def _scrape_data(self, url, start_date):
        source_data = self._get_source_data(url)

        if not source_data:
            return None

        for entry in source_data:
            extracted_data = self._extract_data(entry, start_date)

            if extracted_data:
                self.eq_list.append(extracted_data)

    def _get_source_data(self, url):
        webpage = requests.get(url, verify=PHIVOLCS_CA_CERT_PATH)
        webpage = BeautifulSoup(webpage.text, 'html.parser')

        source_data = self._get_eq_data_table(webpage)

        return source_data

    def _get_eq_data_table(self, webpage):
        eq_data_table = webpage.find_all("table")[2]("tr")[1:]
        return eq_data_table

    def _extract_data(self, entry, start_date):
        eq_date = self._get_date(entry)

        if eq_date is None:
            return None

        if start_date:
            if self._is_date_before_start_date(eq_date, start_date):
                return None

        # Get all other necessary eq details
        eq_location = self._get_location(entry)
        eq_magnitude = self._get_magnitude(entry)
        eq_latitude, eq_longitude = self._get_coordinates(entry)
        eq_depth = self._get_depth(entry)
        eq_event_details_url = self._get_event_details_url(entry)
        eq_graphic_url = self._get_graphic_url(entry)

        # Organize data into a dictionary object and return the object
        eq_entry_details = {
            "date": eq_date,
            "location": eq_location,
            "magnitude": eq_magnitude,
            "coordinates": {
                "latitude": eq_latitude,
                "longitude": eq_longitude
            },
            "depth": eq_depth,
            "event_details_url": eq_event_details_url,
            "graphic_url": eq_graphic_url,
        }

        return eq_entry_details 

    def _get_date(self, entry):
        """
        Extracts the date from the entry and removes extra spaces around words,
        as well as non-printable characters.
        """
        raw_date_str = entry.find_all("td")[0].text
        cleaned_date_str = raw_date_str.strip()  # Strip leading and trailing whitespace characters
        cleaned_date_str = re.sub(NON_PRINTABLE_CHAR_PATTERN, "", cleaned_date_str)
        match = re.match(DATE_REGEX_PATTERN["PHIVOLCS"], cleaned_date_str)

        if match:
            date = f"{match.group(2)} {match.group(3)} {match.group(4)} - {match.group(5)}"
            formatted_date = convert_to_datetime_obj(date, source="PHIVOLCS")

            return formatted_date

        return None

    def _get_location(self, entry):
        """
        Extracts the location and returns it as a string
        """
        location = entry.find_all("td")[5].text.strip()
        location = re.sub(r"Â+", "", location)
        location = re.sub(r"\s+", " ", location)

        return location

    def _get_magnitude(self, entry):
        magnitude = float(entry.find_all("td")[4].text.strip())

        return magnitude

    def _get_coordinates(self, entry):
        latitude = self._get_latitude(entry)
        longitude = self._get_longitude(entry)

        return latitude, longitude

    def _get_latitude(self, entry):
        latitude = float(entry.find_all("td")[1].text.strip())

        if self._is_empty_value(latitude):
            return None

        return latitude

    def _get_longitude(self, entry):
        longitude = float(entry.find_all("td")[2].text.strip())

        if self._is_empty_value(longitude):
            return None

        return longitude

    def _get_depth(self, entry):
        depth = int(entry.find_all("td")[3].text.strip())

        return depth

    def _get_event_details_url(self, entry):
        BASE_URL = r"https://earthquake.phivolcs.dost.gov.ph/"
        SUBDIRECTORY_URL = entry.find("a")["href"]
        eq_details_link = BASE_URL + SUBDIRECTORY_URL

        return eq_details_link

    def _get_graphic_url(self, entry):
        """
        Returns an HTML link that contains an image of the earthquake location.
        This uses the link retrieved from the anchor tag that contains the earthquake
        details link (since it is also identical to the image link), which is then
        processed through RegEx to change the word "html" to "jpg", and append
        the base URL to it. After that, it will return a string containing the
        image link.
        """
        retrieve_date = entry.find("a")
        raw_link = re.sub("html", "jpg", retrieve_date["href"])
        base_url = "https://earthquake.phivolcs.dost.gov.ph/"
        image_link = base_url + raw_link

        return image_link

    def _is_empty_value(self, str):
        if str == "-":
            return True


class PHIVOLCSScraperAlt2(PHIVOLCSScraper):
    def _get_eq_data_table(self, webpage):
        eq_data_table = webpage.find_all("table")[1]("tr")
        return eq_data_table


class PHIVOLCSScraperAlt3(PHIVOLCSScraper):
    def _get_eq_data_table(self, webpage):
        eq_data_table = webpage.find_all("table")[3]("tr")
        return eq_data_table


def scrape_data(URL: str, start_date: str):
    """
    There are other 2 versions of data scraper made for PHIVOLCS to support data scraping
    for old pages since the main scraper doesn't work on them due to different HTML element
    structure of eq data. 

    This function basically uses the main scraper to scrape data. If it doesn't work, it will
    use another scraper. If scraping works, eq_list must contain all the data that are scraped,
    thus returning the eq_list data 
    """
    scrapers = [PHIVOLCSScraper, PHIVOLCSScraperAlt2, PHIVOLCSScraperAlt3]

    for scraper in scrapers:
        eq_list = scraper(URL, start_date)

        if eq_list:
            break

    return eq_list
