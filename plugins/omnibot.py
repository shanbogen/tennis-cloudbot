import random
import os
import datetime

from cloudbot import hook
from cloudbot.markovbot.markovbot import MarkovBot

OMNIFACT_ADDERS = ['stevejhgla', 'thebogbog', 'kingoftrex', 'hoglahoo']
TEXT_LENGTH = 10
SEED_WORDS = ['meat', 'vegan']


@hook.regex(r"\W*([Bb])\W*")
def spew_at_random(chan, message, bot):
    if random.choice([False] * 100 + [True]):
        print("spewing")
        book = os.path.join(bot.data_dir, u'concerned_omnivore_comments.txt')
        tweetbot = MarkovBot()
        tweetbot.read(book)
        tweetbot_text = tweetbot.generate_text(TEXT_LENGTH, seedword=SEED_WORDS)
        message(tweetbot_text, chan)


@hook.command("omnivore", "omni", "bloodmouth")
def tennisfact(message, bot, text, nick, chan):
    if not (text.strip() == "" or text[0:3] == "add"):
        message(nick + ": you must type .omnivore with nothing after it.")
    elif text[0:3] == "add" and nick in OMNIFACT_ADDERS:
        with open(os.path.join(bot.data_dir, "concerned_omnivore_comments.txt"), 'a') as f:
            f.write(text[3:].strip() + ' ')
            message("Your grievance has been added: " + text[3:].strip(), chan)
    elif text[0:3] == "add":
        return "You don't have permission to do that."
    else:
        book = os.path.join(bot.data_dir, u'concerned_omnivore_comments.txt')
        tweetbot = MarkovBot()
        tweetbot.read(book, overwrite=True)
        tweetbot_text = tweetbot.generate_text(TEXT_LENGTH, seedword=SEED_WORDS)
        message(tweetbot_text, chan)


@hook.regex(r"\W*([Vv]egan)\W*")
def hi_tofu(message, chan, bot):
    print('found the vegan')
    if random.sample([True, False, False, False, False, False, False], 1)[0]:
        message("Found the vegan.", chan)
    elif random.sample([True, False, False, False], 1)[0]:
        book = os.path.join(bot.data_dir, u'concerned_omnivore_comments.txt')
        tweetbot = MarkovBot()
        tweetbot.read(book, overwrite=True)
        tweetbot_text = tweetbot.generate_text(TEXT_LENGTH, seedword=SEED_WORDS)
        message(tweetbot_text, chan)


@hook.command("isittuesday")
def isittuesday():
    if datetime.datetime.today().weekday() == 1:
        return 'yes'
    else:
        return 'no'
