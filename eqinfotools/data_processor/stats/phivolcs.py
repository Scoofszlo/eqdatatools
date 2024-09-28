from ._base import StatsGenerator


class PHIVOLCSStatsGenerator(StatsGenerator):
    def _get_eq_list_overview_dict(self):
        eq_list_overview = super()._get_eq_list_overview_dict()
        eq_list_overview["strongest"]["event_details_url"] = None
        eq_list_overview["strongest"]["graphic_url"] = None
        eq_list_overview["weakest"]["event_details_url"] = None
        eq_list_overview["weakest"]["graphic_url"] = None

        return eq_list_overview

    def _set_date_range(self, eq_list, eq_list_overview):
        start_date = eq_list[-1]["date"]
        end_date = eq_list[0]["date"]

        super()._set_date_range(start_date, end_date, eq_list_overview)

    def _set_as_strongest_eq(self, entry, eq_list_overview):
        super()._set_as_strongest_eq(entry, eq_list_overview)
        eq_list_overview["strongest"]["event_details_url"] = entry["event_details_url"]
        eq_list_overview["strongest"]["graphic_url"] = entry["graphic_url"]

    def _set_as_weakest_eq(self, entry, eq_list_overview):
        super()._set_as_weakest_eq(entry, eq_list_overview)
        eq_list_overview["weakest"]["event_details_url"] = entry["event_details_url"]
        eq_list_overview["weakest"]["graphic_url"] = entry["graphic_url"]


def get_stats(eq_list):
    eq_list_overview = PHIVOLCSStatsGenerator(eq_list)

    return eq_list_overview
