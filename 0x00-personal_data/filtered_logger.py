#!/usr/bin/env python3
"""
Filtered Logger Module
"""
import logging
import os
import mysql.connector
from typing import List, Tuple


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str, separator: str) -> str:
    """ Returns the log message obfuscated. """
    import re
    pattern = r"({})=([^{}]*)".format("|".join(fields), separator)
    return re.sub(pattern, r"\1={}".format{redaction}, message)


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


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


def main():
    """ Main function. """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
      "SELECT name, email, phone, ssn, password, ip,"
      "last_login, user_agent FROM users;"
    )
    logger = get_logger()
    for row in cursor:
        log_message = (
            "name={}; email={}; phone={}; ssn={};"
            "password={}; ip={}; last_login={}; user_agent={};"
            .format(*row))
        logger.info(log_message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
