from ._base import DisplayEQData


class PHIVOLCSDisplayEQData(DisplayEQData):
    def display_all_entries(self,
                            location=True,
                            date=True,
                            coordinates=True,
                            depth=True,
                            magnitude=True,
                            link=True,
                            image=True
                            ):

        attributes_to_display = []

        if location:
            attributes_to_display.append(["Location", "location"])
        if date:
            attributes_to_display.append(["Date", "date"])
        if coordinates:
            attributes_to_display.append(["Coordinates", "coordinates"])
        if depth:
            attributes_to_display.append(["Depth", "depth"])
        if magnitude:
            attributes_to_display.append(["Magnitude", "magnitude"])
        if link:
            attributes_to_display.append(["EQ Details Link", "event_details_url"])
        if image:
            attributes_to_display.append(["Image Link", "graphic_url"])

        for every_entry in self._eq_list:
            for attribute in attributes_to_display:
                print(f"{attribute[0]}: {every_entry[attribute[1]]}")
            print()
