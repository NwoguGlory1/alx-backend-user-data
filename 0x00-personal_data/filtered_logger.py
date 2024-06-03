#!/usr/bin/env python3
""" """
import re
import logging


def filter_datum(fields, redaction, message, separator) -> str:
    pattern = f"({'|'.join(f'{re.escape(field)}=.*?(?={re.escape(separator)}|$)' for field in fields)})"
    return re.sub(
            pattern, lambda m: m.group().split('=')[0] + '=' + redaction, message)
    
    class RedactingFormatter(logging.Formatter):
        """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError
