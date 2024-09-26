from ._base import DisplayEQData


class JMADisplayEQData(DisplayEQData):
    def _get_strongest_eq_location(self):
        return self._eq_stats["strongest"]["location"]["location_en"]

    def _get_weakest_eq_location(self):
        return self._eq_stats["weakest"]["location"]["location_en"]

    def display_all_entries(self,
                            location=True,
                            date=True,
                            magnitude=True,
                            link=True,
                            ):

        attributes_to_display = []

        if location:
            attributes_to_display.append(["Location", "location"])
        if date:
            attributes_to_display.append(["Date", "date"])
        if magnitude:
            attributes_to_display.append(["Magnitude", "magnitude"])
        if link:
            attributes_to_display.append(["EQ Details Link", "event_details_url"])

        for every_entry in self._eq_list:
            for attribute in attributes_to_display:
                if attribute[0] != "Date":
                    print(f"{attribute[0]}: {every_entry[attribute[1]]}")
                else:
                    print(f"Observed Date: {every_entry[attribute[1]]['observed_date']}")
                    print(f"Issuance Date: {every_entry[attribute[1]]['issuance_date']}")
            print()
