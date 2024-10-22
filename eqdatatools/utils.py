from datetime import datetime, timezone, timedelta
from eqdatatools.constants import VALID_DATE_FORMATS


def get_datetime_as_iso(datetime_str, source):
    datetime_obj = convert_to_datetime_obj(datetime_str, source)
    formatted_datetime = datetime_obj.isoformat()

    return formatted_datetime


def convert_to_datetime_obj(datetime_str, source):
    if source == "PHIVOLCS":
        valid_date_formats = VALID_DATE_FORMATS["PHIVOLCS"]
        tzinfo = timezone(timedelta(hours=8))

    elif source == "JMA":
        valid_date_formats = VALID_DATE_FORMATS["JMA"]

    for date_format in valid_date_formats:
        try:
            datetime_obj = datetime.strptime(datetime_str, date_format)
            datetime_obj = datetime_obj.replace(tzinfo=tzinfo)
            break
        except ValueError:
            continue

    return datetime_obj
