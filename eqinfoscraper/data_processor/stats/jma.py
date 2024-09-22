def get_stats(eq_list):
    """
    Sets the information overview based from eq_list
    """
    eq_list_overview = {
        "date_range": {
            "start_date": None,
            "end_date": None,
        },
        "strongest": {
            "date": None,
            "location": None,
            "magnitude": None,
            "max_seismic_intensity": None,
            "coordinates": None,
            "depth": None,
            "event_details_url": None,
        },
        "weakest": {
            "date": None,
            "location": None,
            "magnitude": None,
            "max_seismic_intensity": None,
            "coordinates": None,
            "depth": None,
            "event_details_url": None,
        },
        "recorded_eqs": {
            "total": 0,
            "total_per_day": {},
            "total_per_magnitude": {
                "unspecified": 0,
                "m8_0_or_greater": 0,
                "m6_to_7_9": 0,
                "m4_0_to_5_9": 0,
                "below_m4_0": 0,
            }
        }
    }

    _set_date_range(eq_list, eq_list_overview)

    for entry in eq_list:
        _set_if_strongest_eq(entry, eq_list_overview)
        _set_if_weakest_eq(entry, eq_list_overview)
        _set_total_recorded_eqs(entry, eq_list_overview)

    return eq_list_overview


def _set_date_range(eq_list, eq_list_overview):
    """
    Gets the date range from the list of earthquake entries by retrieving
    the date of first recorded earthquake, which will become the start date
    and also by retrieving the date of last recorded earthquake, which will
    become the end date. Thus, this will set the date range for the
    eq_list_overview 
    """
    start_date = eq_list[-1]["date"]["observed_date"]
    end_date = eq_list[0]["date"]["observed_date"]

    eq_list_overview["date_range"]["start_date"] = start_date
    eq_list_overview["date_range"]["end_date"] = end_date


def _set_if_strongest_eq(entry, eq_list_overview):
    magnitude = entry["magnitude"]

    if _eq_is_stronger_than_current_strongest(magnitude, eq_list_overview):
        eq_list_overview["strongest"]["date"] = entry["date"]
        eq_list_overview["strongest"]["location"] = entry["location"]
        eq_list_overview["strongest"]["magnitude"] = entry["magnitude"]
        eq_list_overview["strongest"]["max_seismic_intensity"] = entry["max_seismic_intensity"]
        eq_list_overview["strongest"]["coordinates"] = entry["coordinates"]
        eq_list_overview["strongest"]["depth"] = entry["depth"]
        eq_list_overview["strongest"]["event_details_url"] = entry["event_details_url"]


def _set_if_weakest_eq(entry, eq_list_overview):
    magnitude = entry["magnitude"]

    if _eq_is_weaker_than_current_weakest(magnitude, eq_list_overview):
        eq_list_overview["weakest"]["date"] = entry["date"]
        eq_list_overview["weakest"]["location"] = entry["location"]
        eq_list_overview["weakest"]["magnitude"] = entry["magnitude"]
        eq_list_overview["weakest"]["max_seismic_intensity"] = entry["max_seismic_intensity"]
        eq_list_overview["weakest"]["coordinates"] = entry["coordinates"]
        eq_list_overview["weakest"]["depth"] = entry["depth"]
        eq_list_overview["weakest"]["event_details_url"] = entry["event_details_url"]


def _set_total_recorded_eqs(entry, eq_list_overview):
    magnitude = entry["magnitude"]
    day = int(entry["date"]["observed_date"][8:10])

    _set_total_recorded_eqs_by_mag(magnitude, eq_list_overview)
    _increment_total(eq_list_overview)
    _increment_total_by_day(day, eq_list_overview)


def _increment_total(eq_list_overview):
    eq_list_overview["recorded_eqs"]["total"] += 1


def _increment_total_by_day(day, eq_list_overview):
    if day not in eq_list_overview["recorded_eqs"]["total_per_day"]:
        eq_list_overview["recorded_eqs"]["total_per_day"][day] = 0

    eq_list_overview["recorded_eqs"]["total_per_day"][day] += 1


def _set_total_recorded_eqs_by_mag(magnitude, eq_list_overview):
    if magnitude is None:
        eq_list_overview["recorded_eqs"]["total_per_magnitude"]["unspecified"] += 1
        return

    if float(magnitude) < 4.0:
        eq_list_overview["recorded_eqs"]["total_per_magnitude"]["below_m4_0"] += 1
    elif float(magnitude) >= 4.0 and float(magnitude) <= 5.9:
        eq_list_overview["recorded_eqs"]["total_per_magnitude"]["m4_0_to_5_9"] += 1
    elif float(magnitude) >= 6.0 and float(magnitude) <= 7.9:
        eq_list_overview["recorded_eqs"]["total_per_magnitude"]["m6_to_7_9"] += 1
    elif float(magnitude) >= 8.0:
        eq_list_overview["recorded_eqs"]["total_per_magnitude"]["m8_0_or_greater"] += 1


def _eq_is_weaker_than_current_weakest(magnitude, eq_list_overview):
    if not eq_list_overview["weakest"]["magnitude"]:
        return True
    if magnitude is None:
        return False
    if float(eq_list_overview["weakest"]["magnitude"]) > float(magnitude):
        return True


def _eq_is_stronger_than_current_strongest(magnitude, eq_list_overview):
    if not eq_list_overview["strongest"]["magnitude"]:
        return True
    if magnitude is None:
        return False
    if float(eq_list_overview["strongest"]["magnitude"]) < float(magnitude):
        return True
