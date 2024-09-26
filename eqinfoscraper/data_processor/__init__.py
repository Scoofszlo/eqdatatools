from eqinfoscraper import scraper
from eqinfoscraper.data_processor import stats
from eqinfoscraper.data_processor import display


def display_overview(source, eq_list, eq_stats):
    if source == "JMA":
        eq_display = display.JMADisplayEQData(eq_list, eq_stats)
    if source == "PHIVOLCS":
        eq_display = display.PHIVOLCSDisplayEQData(eq_list, eq_stats)

    eq_display.display_overview()


def display_all_entries(source, eq_list, eq_stats):
    if source == "JMA":
        eq_display = display.JMADisplayEQData(eq_list, eq_stats)
    if source == "PHIVOLCS":
        eq_display = display.PHIVOLCSDisplayEQData(eq_list, eq_stats)

    eq_display.display_all_entries()


def get_earthquake_entries(URL, source, cutoff_date):
    if source == "JMA":
        eq_list = scraper.jma.scrape_data(URL, cutoff_date)
    if source == "PHIVOLCS":
        eq_list = scraper.phivolcs.scrape_data(URL, cutoff_date)

    return eq_list


def get_stats(source, eq_list):
    if source == "JMA":
        eq_list_overview = stats.jma.get_stats(eq_list)
    if source == "PHIVOLCS":
        eq_list_overview = stats.phivolcs.get_stats(eq_list)

    return eq_list_overview
