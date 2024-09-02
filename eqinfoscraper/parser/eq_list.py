from eqinfoscraper.scraper import _scrape_data

def get_earthquake_entries(URL, cutoff_date):
    eq_list = _scrape_data(URL, cutoff_date)
    return eq_list
