import re
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from eqinfoscraper.constants import VALID_URL_FORMATS, VALID_DATE_FORMATS
from ._base_scraper import BaseScraper


class JMAScraper(BaseScraper):
    def _is_valid_url(self, url):
        for valid_url_format in VALID_URL_FORMATS["JMA"]:
            if re.match(valid_url_format, url):
                return True
        return False

    def _get_html_content_as_soup(self, url):
        """
        Fetches the HTML content of the specified URL using Selenium.

        This function initializes a headless Chrome WebDriver, navigates to the given URL,
        waits for the presence of a <td> element to ensure the page has loaded, and then
        retrieves the page source.
        """

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "td"))
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            driver.quit()
            return None

        content = driver.page_source
        driver.close()

        soupified_webpage = BeautifulSoup(content, 'html.parser')
        return soupified_webpage

    def _get_eq_data_table(self, webpage):
        eq_data_table = webpage.find("tbody")
        eq_data_table = eq_data_table.find_all("tr")[1:]
        return eq_data_table

    def _extract_data(self, entry, cutoff_date=None):
        """
        Extract each data and return the values in a dictionary object
        """
        # Get date
        eq_observed_date, eq_issuance_date = self._get_date(entry)

        if cutoff_date:
            if self._is_before_cutoff_date(eq_observed_date, cutoff_date):
                return None

        # Get all other necessary eq details
        eq_location = self._get_location(entry)
        eq_magnitude = self._get_magnitude(entry)
        eq_latitude = None
        eq_longitude = None
        eq_depth = None
        eq_event_details_url = self._get_event_details_url(entry)
        eq_graphic_url = None

        # Organize data into a dictionary object and return the object
        eq_entry_details = {
            "date": {
                "observed_date": eq_observed_date,
                "issuance_date": eq_issuance_date
            },
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

    def _is_before_cutoff_date(self, retrieve_date, cutoff_date):
        """
        This ensures no earthquake entries will be extracted when its
        date is before the cutoff date. For example, the cutoff date is
        January 10, 2024 at 11:35 pm. Any earthquake entries before that
        date and time will not be processed.
        """

        for date_format in VALID_DATE_FORMATS["JMA"]:
            try:
                cutoff_date = datetime.strptime(cutoff_date, date_format)
                break
            except ValueError:
                continue
        else:
            raise ValueError("Invalid date format. Please use a valid format.")

        retrieve_date = datetime.strptime(retrieve_date.strip(), "%d %B %Y - %I:%M %p")

        if retrieve_date < cutoff_date:
            return True

    def _get_date(self, entry):
        eq_observed_date = entry.find_all("td")[0].text
        eq_issuance_date = entry.find_all("td")[4].text
        return eq_observed_date, eq_issuance_date

    def _get_location(self, entry):
        """
        Extracts the location and returns it as a string
        """
        location = entry.find_all("td")[1].text
        location = re.sub(r'\s+', ' ', location)

        return location

    def _get_magnitude(self, entry):
        magnitude = entry.find_all("td")[2].text

        return magnitude

    def _get_latitude(self, entry):
        pass

    def _get_longitude(self, entry):
        pass

    def _get_depth(self, entry):
        pass

    def _get_event_details_url(self, entry):
        BASE_URL = "https://www.data.jma.go.jp/multi/quake/"
        first_row = entry.find_all("td")[0]
        link = first_row.find("a")

        return BASE_URL + link["href"]
    
    def _get_graphic_url(self, entry):
        pass


def scrape_data(URL, cutoff_date=None):
    eq_list = JMAScraper(URL, cutoff_date)

    return eq_list
