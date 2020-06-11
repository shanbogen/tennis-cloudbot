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

GENDERS = {'kingoftrex': 'him',
           'stevejhgla': 'him',
           'thebogbog': 'her',
           'Abortion': 'him',
           'charlotte2785': 'her',
           'merokoyui': 'her',
           'hoglahoo': 'him',
           'botlahoo': 'it',
           'ServeBot': 'it',
           'bananabanana': 'her',
           'mcpro': 'him',
           'Frosty': 'him',
           'blekginger': 'him',
           'lowhope': 'him',
           'reblochon': 'her'}

# helper functions

strip_re = re.compile("(\x03|\x02|\x1f|\x0f)(?:,?\d{1,2}(?:,\d{1,2})?)?")
nick_re = re.compile("^[A-Za-z0-9_|.\-\]\[\{\}]*$", re.I)


def strip(string):
    return strip_re.sub('', string)


def translate(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


def is_valid(target):
    """ Checks if a string is a valid IRC nick. """
    if nick_re.match(target):
        return True
    else:
        return False


# colors
@hook.command
def supperscript(text, message, chan):
    message("Mmm, delicious " + text + " for supper!", chan)

@hook.command
def wuote(text):
    return "Perhaps " + text + " can buy you a copy of this: https://www.amazon.com/Creative-Wonders-9708-Slam-Typing/dp/B00002S9XF"

@hook.command()
def bnag(text):
    return "WTF?! Who are you, Dick Cheney with all of his fingers missing?"

@hook.command()
def bfe(text, chan, nick, message):
    message("Well this is awkward " + nick +
            ", the duck doesn't want to be seen in public with someone who can't spell.",
            chan)

@hook.command()
def bagn(text, chan, nick, message):
    message("Your brain jammed! You can try again whenever you get your life together. The world is watching, " +
            nick + ".", chan)

@hook.command()
def ebf(text):
    return "The duck didn't want to be friends. You should try someone more in your league."

@hook.command()
def gentleban(text, chan, message, action):

    if text == "":
        message("That's such a polite way of doing that! Thanks :)", chan)
        return

    user = text.strip()
    if not is_valid(user):
        message("I tried my best, but I can't ban that user :(", chan)
        return

    if user == "boo_bot":
        message("I look forward to the day when I can ban myself.", chan)
        if random.choice([True, False, False]):
            message("s/ban/bang", chan)
        return

    if user == "Frosty":
        action(
            "opens the door, waits patiently for Frosty to leave, whispers 'you go, girl!', and gently closes the door behind him.")
        return

    try:
        pronoun = GENDERS[user]
    except KeyError:
        pronoun = 'him/her'

    action("opens the door, waits patiently for " + user + " to leave, and gently closes the door behind " + pronoun + ".")
