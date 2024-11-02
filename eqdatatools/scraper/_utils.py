from datetime import datetime
from eqdatatools.constants import VALID_DATE_FORMATS, TIMEZONES
from eqdatatools.exceptions import InvalidDateFormat


def convert_to_datetime_obj(datetime_str: str, source: str) -> datetime:
    valid_date_formats = VALID_DATE_FORMATS.get(source)
    tzinfo = TIMEZONES.get(source)

    for date_format in valid_date_formats:
        try:
            datetime_obj = datetime.strptime(datetime_str, date_format)

            if tzinfo:
                datetime_obj = datetime_obj.replace(tzinfo=tzinfo)

            return datetime_obj
        except ValueError:
            continue

    raise InvalidDateFormat(datetime_str)
