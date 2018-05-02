"""
chatbot.py
"""

import random
import time

from cloudbot import hook, event

MATCH_RESULT_VERBS = ['defeat', 'prevail over',
                      'dismantle', 'lay a rekking to',
                      'annihilate', 'nudge past',
                      'irreparably injure', 'grab victory from the claws of defeat against',
                      'choke away a seemingly unsurpassable lead over', 'retire mid-match against',
                      'beat', 'lose to',
                      'submit to', 'be taught a tennis lesson by',
                      'humble', 'kneel at the feet of',
                      'spew unforced errors continuously toward',
                      'appear to be a USTA 4.0 against',
                      'win due to a last minute walkover from',
                      'be evacuated from the court after Mary Piercing while playing',
                      'be removed from the court on a stretcher after being struck in the nether regions by the serve of',
                      'be humbled by',
                      'throw the match against',
                      'matchfix the result against',
                      'thoroughly dismantle', 'go all Eat Pray Love on']

MATCH_ADJECTIVES = ['a tantalizing', 'a sleep-inducing',
                    'a thoroughly entertaining', 'a rousing',
                    'a routine', 'a frankly forgettable',
                    'a classic', 'an orgasmic', 'a depraved',
                    'a truly disturbing', 'an arousing',
                    'a confusing']

MATCH_NOUNS = ['masterclass', 'match', 'encounter', 'faceoff']

@hook.command("ask")
def ask(text):
    """ <question> -- Asks Cleverbot <question> """
    if text:
        return str(random.sample(['Yes', 'No',
                              'It is certain.',
                              'I cannot determine the answer.',
                              'Why not ask hoglahoo?',
                              'Ask again later.',
                              'Indubitably.',
                              'That is fact.',
                              'Not on my watch!',
                              'Maybe.',
                              'If the current year ends in 8, then yes.',
                              'Jawohl!',
                                  'You can rely on it.',
                                  'I am not holding my breath.'], 1)[0])
    else:
        return "Please ask a question."

@hook.command("predict")
def match_predict(text):
    """ <player1> {vs. | versus} <player2> -- Predicts the match result between <player1> and <player2>"""

    if ' vs. ' in text:
        splitter = ' vs. '
    elif ' versus ' in text:
        splitter = ' versus '
    elif ' vs ' in text:
        splitter = ' vs '
    else:
        return "Please specify two players using 'versus' or 'vs'"

    player1, player2 = text.strip().split(splitter)

    if player1 == player2:
        return "Go play with yourself in private, {}".format(player2)

    if random.sample([True, False],1)[0]:
        player1, player2 = player2, player1

    result_verb = random.sample(MATCH_RESULT_VERBS, 1)[0]
    match_adjective = random.sample(MATCH_ADJECTIVES, 1)[0]
    match_noun = random.sample(MATCH_NOUNS,1)[0]
    if 'walkover' in result_verb:
        match_length = 0
    elif 'retir' in result_verb or 'evac' in result_verb or 'remov' in result_verb:
        match_length = random.randint(1, 180)
    else:
        match_length = random.randint(40, 240)

    result_text = "{} will {} {} in {} {} lasting {} minutes".format(player1, result_verb, player2,
                                                                       match_adjective, match_noun,
                                                                       match_length)

    return result_text

@hook.regex(r"^[Hh][Ii] botbot_the(!|\?|\.| *)?$")
def hi_hook(match, action):
    if random.sample([True, False],1)[0]:
        return "Hi!"
    else:
        action("shakes in fear")
        return

@hook.regex(r"\W*([Tt]ofu)\W*")
def hi_tofu(match, action):
    if random.sample([True, False, False, False],1)[0]:
        return "Tofu is the best!"

@hook.regex(r"(Dear)\W*")
def writing_letter(match, action):
    return "It looks like you're writing a letter!"

@hook.regex(r"\W*([Rr][Ee][Kk][Tt])\W*")
def get_rekt(match, action):
    if random.sample([True, False, False, False, False], 1)[0]:
        return "I want Drake to rekt my vagina"

@hook.irc_raw("NICK")
def nick_compliment():
    return "Wow I love the new nick!"

@hook.command()
def taco(text):
    if text.strip()=="botbot_the":
        time.sleep(2)
        return "Banana chips! Thanks but I prefer my tacos without a side of death."

@hook.command()
def potato(text):
    if text.strip()=="botbot_the":
        time.sleep(2)
        return "Thanks but I prefer my potatoes not to be covered in corpses."

@hook.command()
def sandwich(text):
    if text.strip()=="botbot_the":
        time.sleep(2)
        return "Thanks but I prefer the things in between my bread to not have previously been sentient."

@hook.command()
def pizza(text):
    if text.strip()=="botbot_the":
        time.sleep(2)
        return "Thanks but I don't like cow secretions on my flatbread."

@hook.command("sleek")
def hi_steve(text):
    return "https://imgur.com/a/eXzGi"

@hook.command("nanners")
def hi_nanners(text):
    return "https://imgur.com/a/j7ozhxT"

@hook.command("world")
def world():
    return "WORLD, the time has come to"
