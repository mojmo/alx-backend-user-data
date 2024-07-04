#!/usr/bin/env python3

"""
Module for log message filtering with obfuscation

Provides a function to filter log messages by obfuscating specific
fields with a redaction string.
"""

import logging
import mysql.connector
import os
import re
from typing import List, Tuple


PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes a RedactingFormatter object.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a log record.
        """
        original_message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, original_message,
                            self.SEPARATOR)


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """
    Filters a log message by obfuscating specified fields.

    Args:
        fields: List of field names to obfuscate.
        redaction: String to replace the value of obfuscated fields.
        message: The log message string.
        separator: Character separating fields in the log message.

    Returns:
        The filtered log message with obfuscated fields.
    """
    pattern = '|'.join([f'{field}=[^{separator}]*' for field in fields])
    return re.sub(pattern, lambda m: f'{m.group().split("=")[0]}={redaction}',
                  message)


def get_logger() -> logging.Logger:
    """Creates a logger for user data with a redacting formatter"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Creates a database connection"""
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connection.MySQLConnection(
        user=db_user,
        password=db_pwd,
        host=db_host,
        database=db_name,
    )

    return connection


def main():
    """
    Retrieve all rows in the users table and display
    each row under a filtered format
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()

    field_names = [i[0] for i in cursor.description]
    for row in cursor.fetchall():
        record = {field_names[i]: row[i] for i in range(len(field_names))}
        log_msg = "; ".join(
            [f"{key}={value}" for key, value in record.items()])
        logger.info(log_msg)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
