#!/usr/bin/env python3
"""
Filtered Logger Module
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """ Returns the log message obfuscated. """
    return re.sub(
        '|'.join([f'{field}=[^{separator}]*' for field in fields]),
        lambda m: f"{m.group().split('=')[0]}={redaction}",
        message
    )
