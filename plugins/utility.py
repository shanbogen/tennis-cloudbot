"""
utility.py

Provides a number of simple commands for working with strings.

Created By:
    - Luke Rogers <https://github.com/lukeroge>
    - Dabo Ross <https://github.com/daboross>

Special Thanks:
    - Fletcher Boyd <https://github.com/thenoodle68>

License: GPL v3
"""

import base64
import hashlib
import collections
import re
import os
import json
import codecs
import urllib.parse
import random
import binascii

from cloudbot import hook
from cloudbot.util import formatting, web, colors


COLORS = collections.OrderedDict([
    ('red', '\x0304'),
    ('orange', '\x0307'),
    ('yellow', '\x0308'),
    ('green', '\x0309'),
    ('cyan', '\x0303'),
    ('ltblue', '\x0310'),
    ('rylblue', '\x0312'),
    ('blue', '\x0302'),
    ('magenta', '\x0306'),
    ('pink', '\x0313'),
    ('maroon', '\x0305')
])

# helper functions

strip_re = re.compile("(\x03|\x02|\x1f|\x0f)(?:,?\d{1,2}(?:,\d{1,2})?)?")


def strip(string):
    return strip_re.sub('', string)


def translate(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


# colors
@hook.command
def supperscript(text):
    return "Mmm, delicious " + text + " for supper!"

@hook.command
def wuote(text):
    return "Perhaps " + text + " can buy you a copy of this: https://www.amazon.com/Creative-Wonders-9708-Slam-Typing/dp/B00002S9XF"

@hook.command()
def bnag(text):
    return "WTF?! Who are you, Dick Cheney with all of his fingers missing?"

@hook.command()
def bfe(text):
    return "Well this is awkward, the duck doesn't want to be seen in public with someone who can't spell."

@hook.command()
def bagn(text):
    return "Your brain jammed! You can try again whenever you get your life together."

@hook.command()
def ebf(text):
    return "The duck didn't want to be friends. You should try someone more in your league."
