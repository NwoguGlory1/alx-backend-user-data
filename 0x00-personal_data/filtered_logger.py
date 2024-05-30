#!/usr/bin/env python3
""" """
import re


def filter_datum(fields, redaction, message, separator):
    pattern = f"({'|'.join(f'{re.escape(field)}=.*?(?={re.escape(separator)}|$)' for field in fields)})"
    return re.sub(
            pattern, lambda m: m.group().split('=')[0] + '=' + redaction, message)
