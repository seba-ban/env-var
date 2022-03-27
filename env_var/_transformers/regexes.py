import re
from typing import Pattern

hostname_regex = re.compile(
    r"^(?=.{1,253}\.?$)[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[-0-9a-z]{0,61}[0-9a-z])?)*\.?$",
    re.IGNORECASE,
)

url_regex = re.compile(
    r"^(?:https?|ftp):\/\/(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z0-9\u00a1-\uffff]+-)*[a-z0-9\u00a1-\uffff]+)(?:\.(?:[a-z0-9\u00a1-\uffff]+-)*[a-z0-9\u00a1-\uffff]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/[^\s]*)?$",
    re.IGNORECASE | re.UNICODE,
)

uuid_regex = re.compile(
    r"^(?:urn:uuid:)?[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}$", re.IGNORECASE
)

uri_regex = re.compile(r"^(?:[a-z][a-z0-9+\-.]*:)(?:\/?\/)?[^\s]*$", re.IGNORECASE)

email_regex = re.compile(
    r"^[a-z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)*$",
    re.IGNORECASE,
)


def regex_transformer_factory(pattern: Pattern[str]):
    def transformer(s: str):
        if re.match(pattern, s):
            return s
        raise ValueError(f'"{s}" doesn\'t match pattern "{pattern}"')

    return transformer
