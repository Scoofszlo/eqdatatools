from datetime import timezone, timedelta
import os


def get_ca_cert_file_path():
    """
    Ensures that CA certificate file is imported properly regardless
    of where script is being executed.
    """
    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    _PHIVOLCS_CA_CERT_RELATIVE_PATH = os.path.join("..", "phivolcs_ca_cert", "phivolcs-dost-gov-ph-chain.pem")
    return os.path.abspath(os.path.join(_BASE_DIR, _PHIVOLCS_CA_CERT_RELATIVE_PATH))


PHIVOLCS_CA_CERT_PATH = get_ca_cert_file_path()
PHIVOLCS_HOME_URL = "https://earthquake.phivolcs.dost.gov.ph/"

VALID_URL_FORMATS = {
    "PHIVOLCS": [
        r"^https?:\/\/earthquake.phivolcs.dost.gov.ph\/?$",
        r"^https?:\/\/earthquake.phivolcs.dost.gov.ph\/?EQLatest-Monthly\/[2][0](([1][7-9])|[2][0-4])\/[\w\.?]+\/?$"
    ],
    "JMA": [
        r"^https?:\/\/www.jma.go.jp\/bosai\/quake\/data\/list.json$"
    ]
}

VALID_DATE_FORMATS = {
    "DEFAULT": [
        "%Y-%m-%dT%H:%M:%S%z"
    ],
    "PHIVOLCS": [
        "%d %B %Y - %I:%M %p",
        "%d %b %Y - %I:%M %p",
        "%Y%m%d_%H%M"
    ],
    "JMA": [
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y/%m/%d %H:%M",
        "%Y%m%d_%H%M"
    ]
}

TIMEZONES = {
    "PHIVOLCS": timezone(timedelta(hours=8)),
    "JMA": None  # JMA dates are always in UTC time
}

DATE_REGEX_PATTERN = {
    "PHIVOLCS": r"((\d{2})\s+(\w+)\s+(\d{4})\s+-\s+(\d{2}:\d{2}\s+[AaPp][Mm]))"
}

# Pattern to match non-printable characters
NON_PRINTABLE_CHAR_PATTERN = r"[^\x20-\x7E]"
