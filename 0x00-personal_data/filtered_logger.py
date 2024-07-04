#!/usr/bin/env python3

"""
Module for log message filtering with obfuscation

Provides a function to filter log messages by obfuscating specific
fields with a redaction string.
"""

import re


def filter_datum(
        fields: list[str],
        redaction: str,
        message: str,
        separator: str
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
    pattern = '|'.join([f'({field}=.*?{separator})' for field in fields])
    pattern = f'({pattern})'
    return re.sub(
        pattern,
        lambda m: f'{m.group(0).split("=")[0]}={redaction}{separator}', message
        )
