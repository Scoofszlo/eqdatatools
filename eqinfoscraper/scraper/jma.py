import re
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from eqinfoscraper.exceptions import InvalidURLError
from eqinfoscraper.constants import VALID_URL_FORMATS, VALID_DATE_FORMATS

def scrape_data(URL, cutoff_date=None):
    """
    Scrapes data from the specified URL
    """

    webpage = _get_html_content(URL)
    soupified_page = BeautifulSoup(webpage, 'html.parser')
    table = soupified_page.find("tbody")
    eq_entries_table = table.find_all("tr")[1:]

    # Loop through each row of data from the table to extract them and
    # put them into a list
    eq_list = []
    for entry in eq_entries_table:
        data = _extract_data(entry, cutoff_date)
        if data:
            eq_list.append(data)

    return eq_list

def _get_html_content(URL):
    """
    Fetches the HTML content of the specified URL using Selenium.

    This function initializes a headless Chrome WebDriver, navigates to the given URL,
    waits for the presence of a <td> element to ensure the page has loaded, and then
    retrieves the page source.
    """

    if not _is_valid_url(URL):
        raise InvalidURLError(URL)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.get(URL)

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
    return content

def _extract_data(entry, cutoff_date=None):
    """
    Extract each data and return the values in a dictionary object
    """

    # Get date
    eq_observed_date = entry.find_all("td")[0].text

    if cutoff_date:
        if _is_before_cutoff_date(eq_observed_date, cutoff_date):
            return None

    # Get all other necessary eq details
    eq_location = entry.find_all("td")[1].text
    eq_location = re.sub(r'\s+', ' ', eq_location) # Removes extra spaces between words
    eq_magnitude = entry.find_all("td")[2].text
    eq_max_seismic_intensity = entry.find_all("td")[3].text
    eq_issuance_date = entry.find_all("td")[4].text
    eq_details_link = _get_eq_details_link(entry)

    # Organize data into a dictionary object and return the object
    eq_entry_details = {
        "location": eq_location,
        "date": {
            "observed_date": eq_observed_date,
            "issuance_date": eq_issuance_date
        },
        "magnitude": eq_magnitude,
        "max_seismic_intensity": eq_max_seismic_intensity, 
        "eq_details_link": eq_details_link,
    }

    return eq_entry_details

def _is_valid_url(URL):
    """
    Checks the URL if it is one of the valid URLs supported for extraction
    of data.
    """

    for valid_url_format in VALID_URL_FORMATS["JMA"]:
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

    for date_format in VALID_DATE_FORMATS["JMA"]:
        try:
            cutoff_date = datetime.strptime(cutoff_date, date_format)
            break
        except ValueError:
            continue
    else:
        raise ValueError("Invalid date format. Please use a valid format.")

    retrieve_date = datetime.strptime(retrieve_date.text.strip(), "%Y/%m/%d %H:%M")

    if retrieve_date < cutoff_date:
        return True

def _get_eq_details_link(entry):
    BASE_URL = "https://www.data.jma.go.jp/multi/quake/"
    first_row = entry.find_all("td")[0]
    link = first_row.find("a")

    return BASE_URL + link["href"]
