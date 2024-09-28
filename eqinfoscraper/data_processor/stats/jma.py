from ._base import StatsGenerator


class JMAStatsGenerator(StatsGenerator):
    def _get_eq_list_overview_dict(self):
        eq_list_overview = super()._get_eq_list_overview_dict()
        eq_list_overview["strongest"]["max_seismic_intensity"] = None
        eq_list_overview["strongest"]["event_details_url"] = None
        eq_list_overview["weakest"]["max_seismic_intensity"] = None
        eq_list_overview["weakest"]["event_details_url"] = None

        return eq_list_overview

    def _set_date_range(self, eq_list, eq_list_overview):
        start_date = eq_list[-1]["date"]["observed_date"]
        end_date = eq_list[0]["date"]["observed_date"]

        super()._set_date_range(start_date, end_date, eq_list_overview)

    def _set_as_strongest_eq(self, entry, eq_list_overview):
        super()._set_as_strongest_eq(entry, eq_list_overview)
        eq_list_overview["strongest"]["max_seismic_intensity"] = entry["max_seismic_intensity"]
        eq_list_overview["strongest"]["event_details_url"] = entry["event_details_url"]

    def _set_as_weakest_eq(self, entry, eq_list_overview):
        super()._set_as_weakest_eq(entry, eq_list_overview)
        eq_list_overview["weakest"]["max_seismic_intensity"] = entry["max_seismic_intensity"]
        eq_list_overview["weakest"]["event_details_url"] = entry["event_details_url"]


def get_stats(eq_list):
    eq_list_overview = JMAStatsGenerator(eq_list)

    return eq_list_overview
