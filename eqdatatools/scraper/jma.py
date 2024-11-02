import json
import re
import requests
from eqdatatools.constants import VALID_URL_FORMATS
from eqdatatools.exceptions import InvalidCoordinatesFormat, InvalidDepthFormat
from eqdatatools.scraper._utils import convert_to_datetime_obj
from ._base import DataScraper


class JMAScraper(DataScraper):
    def _is_valid_url(self, url):
        for valid_url_format in VALID_URL_FORMATS["JMA"]:
            if re.match(valid_url_format, url):
                return True
        return False

    def _scrape_data(self, url, start_date):
        data = self._get_json_data(url)

        for entry in data:
            data = self._extract_data(entry, start_date)

            if not data or self._is_data_duplicate(data):
                continue

            self.eq_list.append(data)

    def _get_json_data(self, url):
        response = requests.get(url)

        if response.status_code == 200:
            data = json.loads(response.text)
            return data
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None

    def _extract_data(self, entry, start_date):
        eq_observed_date, eq_issuance_date = self._get_date(entry)

        if start_date:
            if self._is_date_before_start_date(eq_observed_date, start_date):
                return None

        eq_location_en, eq_location_jpn = self._get_location(entry)
        eq_magnitude = self._get_magnitude(entry)
        eq_max_seismic_intensity = self._get_max_seismic_intensity(entry)
        eq_latitude, eq_longitude = self._get_coordinates(entry)
        eq_depth = self._get_depth(entry)
        eq_event_details_url = self._get_event_details_url(entry)

        eq_entry_details = {
            "date": {
                "observed_date": eq_observed_date,
                "issuance_date": eq_issuance_date
            },
            "location": {
                "location_en": eq_location_en,
                "location_jpn": eq_location_jpn
            },
            "magnitude": eq_magnitude,
            "max_seismic_intensity": eq_max_seismic_intensity,
            "coordinates": {
                "latitude": eq_latitude,
                "longitude": eq_longitude
            },
            "depth": eq_depth,
            "event_details_url": eq_event_details_url,
        }

        return eq_entry_details

    def _get_date(self, entry):
        eq_observed_date = convert_to_datetime_obj(entry["at"], source="JMA")
        eq_issuance_date = convert_to_datetime_obj(entry["rdt"], source="JMA")

        return eq_observed_date, eq_issuance_date

    def _get_location(self, entry):
        location_en = self._remove_extra_characters(entry["en_anm"])
        location_jpn = entry["anm"]

        return location_en, location_jpn

    def _get_magnitude(self, entry):
        if entry["mag"] == "":
            return None

        magnitude = float(entry["mag"])

        if magnitude == "":
            return None

        return magnitude

    def _get_max_seismic_intensity(self, entry):
        if entry["maxi"] == "":
            return None

        max_seismic_intensity = int(entry["maxi"])

        return max_seismic_intensity

    def _get_coordinates(self, entry):
        pattern = r'([+-]\d+\.\d+)([+-]\d+\.\d+)'
        match = re.match(pattern, entry["cod"])

        if match:
            latitude = float(match.group(1))
            longitude = float(match.group(2))

            return latitude, longitude
        elif entry["cod"] == "":
            return None, None
        else:
            raise InvalidCoordinatesFormat(entry["cod"], pattern)

    def _get_depth(self, entry):
        pattern = r'(?:[+-]\d+\.\d+)(?:[+-]\d+\.\d+)([-+]\d+)'
        match = re.match(pattern, entry["cod"])

        if match:
            depth = int(match.group(1))
            depth = int(abs(depth) / 1000)

            return depth
        elif entry["cod"] == "":
            return None
        else:
            raise InvalidDepthFormat(entry["cod"], pattern)

    def _get_event_details_url(self, entry):
        BASE_URL = "https://www.data.jma.go.jp/multi/quake/quake_detail.html?eventID="
        event_id = entry["ctt"]

        return BASE_URL + event_id

    def _remove_extra_characters(self, string):
        pattern = r"\u200b"
        cleaned_str = re.sub(pattern, "", string)

        return cleaned_str

    def _is_data_duplicate(self, data):
        """
        Checks if data to be appended is the same as the previous entry.
        There are some instances where there are entries that has same
        earthquake details for some unknown reason.
        """
        if len(self.eq_list) == 0:
            return False

        entry_to_be_appended = data['date']['observed_date']
        last_appended_entry = self.eq_list[-1]['date']['observed_date']

        if entry_to_be_appended == last_appended_entry:
            return True


def scrape_data(URL, start_date):
    eq_list = JMAScraper(URL, start_date)

    return eq_list
