from datetime import datetime as dt
from django.utils import timezone
from os.path import isfile
from types import SimpleNamespace
import re


def milliseconds(_dt: dt):
    """Returns the milliseconds since epoch from a datetime"""
    return int(
        timezone.localtime(_dt).replace(tzinfo=timezone.utc).timestamp() * 10**3
    )


def num_lines(filename: str):
    """Counts the lines in a file in a efficient way"""

    def blocks(files, size=65536):
        while True:
            b = files.read(size)
            if not b:
                break
            yield b

    cnt = 0
    if isfile(filename):
        with open(filename, "r", encoding="utf-8", errors="ignore") as f:
            cnt = sum(bl.count("\n") for bl in blocks(f))
    return cnt


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [SimpleNamespace(**dict(zip(columns, row))) for row in cursor.fetchall()]


unit_lookup = {
    "us": "microseconds",
    "ms": "milliseconds",
    "s": "seconds",
    "m": "minutes",
    "h": "hours",
    "d": "days",
    "w": "weeks",
}


def value_unit(x: str, default: str) -> tuple[int, str]:
    if x is None:
        x = default
    if x is not None:
        match = re.search(f"^([0-9]+)({'|'.join(unit_lookup.keys())})", x)
        if match:
            return int(match.group(1)), unit_lookup.get(match.group(2))
    # We define a default in case the value cannot be parsed
    return 1, "days"


def quote(s: str):
    return f"'{s}'"
