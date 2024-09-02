import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm
from eqinfoscraper.exceptions import InvalidURLError
from eqinfoscraper.constants import PHIVOLCS_CA_CERT_PATH, VALID_URL_FORMATS, VALID_DATE_FORMATS


def scrape_data(URL, cutoff_date):
    """
    Scrapes data from the specified URL
    """
    if not _is_valid_url(URL):
        raise InvalidURLError(URL)

    # Makes a request to the URL and gets the HTML content,
    # which is then converted to BeautifulSoup object.
    webpage = _get_html_content(URL)
    soupified_page = BeautifulSoup(webpage, 'html.parser')

    # Go to the table that contains the earthquake entries
    eq_entries_table = soupified_page.find_all("table")[2]("tr")[1:]

    # Loop through each row of data from the table to extract them and
    # put them into a list
    eq_list = []
    for entry in tqdm(eq_entries_table, desc="Scraping data"):
        data = _extract_data(entry, cutoff_date)
        if data:
            eq_list.append(data)

    return eq_list

def _get_html_content(URL):
    """
    Makes a request to the specified URL and returns HTML content
    string
    """
    webpage = requests.get(URL, verify=PHIVOLCS_CA_CERT_PATH)
    return webpage.text

    # The code below can be an alternative one
    # http = urllib3.PoolManager(
    #     cert_reqs="CERT_REQUIRED",
    #     ca_certs=PHIVOLCS_CA_CERT_PATH
    # )
    # response = http.request('GET', URL)
    # return response.data

def _extract_data(entry, cutoff_date=None):
    """
    Extract each data and return the values in a dictionary object
    """
    # Get date
    eq_date = entry.find("a")

    if cutoff_date:
        if _is_before_cutoff_date(eq_date, cutoff_date):
            return None

    # Get all other necessary eq details
    eq_latitude = entry.find_all("td")[1].text.strip()
    eq_longitude = entry.find_all("td")[2].text.strip()
    eq_depth = entry.find_all("td")[3].text.strip()
    eq_magnitude = entry.find_all("td")[4].text.strip()
    eq_location = _get_location(entry)
    eq_details_link = str("https://earthquake.phivolcs.dost.gov.ph/" + (eq_date["href"]))
    eq_image_link = _get_image_link(eq_date)

    # Organize data into a dictionary object and return the object
    eq_entry_details = {
        "location": eq_location,
        "date": str(eq_date.text.strip()),
        "coordinates": {
            "latitude": eq_latitude,
            "longitude": eq_longitude
        },
        "depth": eq_depth,
        "magnitude": eq_magnitude,
        "eq_details_link": eq_details_link,
        "image_link": eq_image_link,
    }

    return eq_entry_details

def _is_valid_url(URL):
    """
    Checks the URL if it is one of the valid URLs supported for extraction
    of data.
    """

    for valid_url_format in VALID_URL_FORMATS["PHIVOLCS"]:
        if re.match(valid_url_format, URL):
            return True
    return False

def _is_before_cutoff_date(retrieve_date, cutoff_date):
    """
    This ensures no earthquake entries will be extracted when its
    date is before the cutoff date. For example, the cutoff date is
    January 10, 2024 at 11:35 pm. Any earthquake entries before that
    date and time will not be processed.
    """

    for date_format in VALID_DATE_FORMATS:
        try:
            cutoff_date = datetime.strptime(cutoff_date, date_format)
            break
        except ValueError:
            continue
    else:
        raise ValueError("Invalid date format. Please use a valid format.")

    retrieve_date = datetime.strptime(retrieve_date.text.strip(), "%d %B %Y - %I:%M %p")

    if retrieve_date < cutoff_date:
        return True

def _get_location(entry):
    """
    Extracts the location and returns it as a string
    """
    complete_location = entry.find_all("td")[5].text.strip()
    complete_location = re.sub(r"Â+", "", complete_location)
    complete_location = re.sub(r"\s+", " ", complete_location)

    return complete_location

def _get_image_link(retrieve_date):
    """
    Returns an HTML link that contains an image of the earthquake location.
    This uses the link retrieved from the anchor tag that contains the earthquake
    details link (since it is also identical to the image link), which is then
    processed through RegEx to change the word "html" to "jpg", and append
    the base URL to it. After that, it will return a string containing the
    image link.
    """
    raw_link = re.sub("html", "jpg", retrieve_date["href"])
    base_url = "https://earthquake.phivolcs.dost.gov.ph/"
    image_link = base_url + raw_link

    return image_link
