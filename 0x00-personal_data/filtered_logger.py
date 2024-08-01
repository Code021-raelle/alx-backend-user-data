#!/usr/bin/env python3
"""
Filtered Logger Module
"""
import logging
import re
import os
import mysql.connector
from mysql.connector import connection
from typing import List, Tuple


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


def get_db() -> connection.MySQLConnection:
    """ Returns a connection to the database. """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
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


PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """ Returns a logger object. """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger
