#!/usr/bin/env python3
"""
Filtered Logger Module
"""
import logging
import re
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str, separator: str) -> str:
    """ Returns the log message obfuscated. """
    return re.sub(
        '|'.join([f'{field}=[^{separator}]*' for field in fields]),
        lambda m: f"{m.group().split('=')[0]}={redaction}",
        message
    )


class RedactingFormatter(logging.Formatter):
    """ RedactingFormatter class. """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Initialize the formatter with specific fields to redact. """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format the log record, redacting sensitive fields. """
        original_message = super(RedactingFormatter, self).format(record)
        return filter_datum(
            self.fields, self.REDACTION, original_message, self.SEPARATOR)
