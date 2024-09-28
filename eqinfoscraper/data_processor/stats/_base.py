from abc import ABC, abstractmethod


class StatsGenerator(ABC):
    def __new__(cls, eq_list):
        instance = super(StatsGenerator, cls).__new__(cls)
        eq_list_overview = instance.get_stats(eq_list)

        return eq_list_overview

    def get_stats(self, eq_list):
        eq_list_overview = self._get_eq_list_overview_dict()

        self._set_date_range(eq_list, eq_list_overview)

        for entry in eq_list:
            if self._eq_is_stronger_than_current_strongest(entry["magnitude"], eq_list_overview):
                self._set_as_strongest_eq(entry, eq_list_overview)

            if self._eq_is_weaker_than_current_weakest(entry["magnitude"], eq_list_overview):
                self._set_as_weakest_eq(entry, eq_list_overview)

            self._set_total_recorded_eqs(entry, eq_list_overview)

        return eq_list_overview

    @abstractmethod
    def _get_eq_list_overview_dict(self):
        """Returns a dict containing eq details such as strongest, weakest, and
        total recorded eqs."""

        eq_list_overview = {
            "date_range": {
                "start_date": None,
                "end_date": None,
            },
            "strongest": {
                "date": None,
                "location": None,
                "magnitude": None,
                "coordinates": None,
                "depth": None,
            },
            "weakest": {
                "date": None,
                "location": None,
                "magnitude": None,
                "coordinates": None,
                "depth": None,
            },
            "recorded_eqs": {
                "total": 0,
                "total_per_magnitude": {
                    "unspecified": 0,
                    "m8_0_or_greater": 0,
                    "m6_to_7_9": 0,
                    "m4_0_to_5_9": 0,
                    "below_m4_0": 0,
                }
            }
        }

        return eq_list_overview

    @abstractmethod
    def _set_date_range(self, start_date, end_date, eq_list_overview):
        """
        Gets the date range from the list of earthquake entries by retrieving
        the date of first recorded earthquake, which will become the start date
        and also by retrieving the date of last recorded earthquake, which will
        become the end date. Thus, this will set the date range for the
        eq_list_overview
        """

        eq_list_overview["date_range"]["start_date"] = start_date
        eq_list_overview["date_range"]["end_date"] = end_date

    @abstractmethod
    def _set_as_strongest_eq(self, entry, eq_list_overview):
        """
        Checks if the earthquake being checked is the strongest. If true,
        then it will be set as a strongest earthquake.
        """

        eq_list_overview["strongest"]["date"] = entry["date"]
        eq_list_overview["strongest"]["location"] = entry["location"]
        eq_list_overview["strongest"]["magnitude"] = entry["magnitude"]
        eq_list_overview["strongest"]["coordinates"] = entry["coordinates"]
        eq_list_overview["strongest"]["depth"] = entry["depth"]

    @abstractmethod
    def _set_as_weakest_eq(self, entry, eq_list_overview):
        """
        Checks if the earthquake being checked is the weakest. If true,
        then it will be set as a weakest earthquake.
        """
        eq_list_overview["weakest"]["date"] = entry["date"]
        eq_list_overview["weakest"]["location"] = entry["location"]
        eq_list_overview["weakest"]["magnitude"] = entry["magnitude"]
        eq_list_overview["weakest"]["coordinates"] = entry["coordinates"]
        eq_list_overview["weakest"]["depth"] = entry["depth"]

    def _set_total_recorded_eqs(self, entry, eq_list_overview):
        magnitude = entry["magnitude"]

        self._set_total_recorded_eqs_by_mag(magnitude, eq_list_overview)
        self._increment_total(eq_list_overview)

    def _increment_total(self, eq_list_overview):
        eq_list_overview["recorded_eqs"]["total"] += 1

    def _set_total_recorded_eqs_by_mag(self, magnitude, eq_list_overview):
        if magnitude is None:
            eq_list_overview["recorded_eqs"]["total_per_magnitude"]["unspecified"] += 1
            return

        if magnitude < 4.0:
            eq_list_overview["recorded_eqs"]["total_per_magnitude"]["below_m4_0"] += 1
        elif magnitude >= 4.0 and magnitude <= 5.9:
            eq_list_overview["recorded_eqs"]["total_per_magnitude"]["m4_0_to_5_9"] += 1
        elif magnitude >= 6.0 and magnitude <= 7.9:
            eq_list_overview["recorded_eqs"]["total_per_magnitude"]["m6_to_7_9"] += 1
        elif magnitude >= 8.0:
            eq_list_overview["recorded_eqs"]["total_per_magnitude"]["m8_0_or_greater"] += 1

    def _eq_is_weaker_than_current_weakest(self, magnitude, eq_list_overview):
        if not eq_list_overview["weakest"]["magnitude"]:
            return True
        if magnitude is None:
            return False
        if eq_list_overview["weakest"]["magnitude"] > magnitude:
            return True

    def _eq_is_stronger_than_current_strongest(self, magnitude, eq_list_overview):
        if not eq_list_overview["strongest"]["magnitude"]:
            return True
        if magnitude is None:
            return False
        if eq_list_overview["strongest"]["magnitude"] < magnitude:
            return True
