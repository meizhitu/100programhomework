#!/usr/bin/env python
"""web.py: makes web apps (http://webpy.org)"""

from __future__ import generators

__version__ = "0.37"
__author__ = [
    "Aaron Swartz <me@aaronsw.com>",
    "Anand Chitipothu <anandology@gmail.com>"
]
__license__ = "public domain"
__contributors__ = "see http://webpy.org/changes"

try:
    import webopenid as openid
except ImportError:
    pass # requires openid module

