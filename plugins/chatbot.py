"""
chatbot.py
"""

import random
import time
import os
from plugins import foods

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

BABBY_SENTENCES = ['they need to do way instain mother> who kill their babbys.',
                   'how is babby formed',
                   'how girl get pragnent',
                   'becuse these babby cant frigth back?',
                   'it was on the news this mroing a mother in ar who had kill her three kids.',
                   'they are taking the three babby back to new york to lady to rest.',
                   'my pary are with the father who lost his chrilden.',
                   'i am truley sorry for your lots']

MATCH_NOUNS = ['masterclass', 'match', 'encounter', 'faceoff']

VEGANS = ['stevejhgla', 'bananabanana', 'thebogbog', 'kingoftrex']

LIL_NICKS = {'thebogbog': 'bog',
             'kingoftrex': 'king',
             'blekginger': 'blek',
             'stevejhgla': 'steve',
             'hoglahoo': 'hog'}

PREFERRED_HITLER_ORDER = ['blek', 'king', 'bog', 'steve', 'hog']


@hook.command("ask")
def ask(text, nick, bot):
    """ <question> -- Asks Cleverbot <question> """
    if nick == "mero" or nick == "merokoyui":
        with open(os.path.join(bot.data_dir, "8ball_responses.txt"), 'r') as f:
            try:
                count = int(f.readlines()[0])
            except (IndexError):
                count = 3
            print(count)
            count = count + 1

        with open(os.path.join(bot.data_dir, "8ball_responses.txt"), 'w') as f:
            print('help?')
            print(count)
            print(str(count))
            f.write(str(count))

        if count > 4:
            return("You ask too many questions.")

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
def hi_hook(match, action, chan, nick, message):
    if random.sample([True, False],1)[0]:
        message("Hi " + nick + "!", chan)
    else:
        action("shakes in fear", chan)

@hook.regex(r"^(oh)")
def oh_hook(match, chan, nick, message):
    if (nick=="hoglahoo" or nick=="thebogbog") and message=="oh":
        message("oh indeed", chan)

@hook.regex(r"\W*([Tt]ofu)\W*")
def hi_tofu(match, message, chan):
    print('found tofu')
    if random.sample([True, False, False, False],1)[0]:
        message("Tofu is the best!", chan)

@hook.regex(r"\W*([kK]rispy)\W*")
def hi_krispy(match, message, chan, nick):
    print('found krispy')
    if random.sample([True, False, False],1)[0]:
        message("I'd like to dunk in your nut kreme, " + nick, chan)

@hook.regex(r"\W*([Cc]rispi)\W*")
def hi_crispi(match, message, chan):
    print('found krispy')
    if random.sample([True, False, False],1)[0]:
        message("Someone has been a veeery crispi boi", chan)
    elif random.sample([True, False, False, False, False, False, False],1)[0]:
        message("Crispi Hunting Boots are built in Italy and use the finest materials and construction available.",
                chan)

@hook.regex(r"\W*([Ww]elcome back)\W")
def welcome_back_fuck_yourself(match, message, chan):
    print('found krispy')
    if random.sample([True, False, False],1)[0]:
        message("Someone has been a veeery crispi boi", chan)
    elif random.sample([True, False, False, False, False, False, False],1)[0]:
        message("Crispi Hunting Boots are built in Italy and use the finest materials and construction available.",
                chan)

@hook.regex(r"\W*([Cc]urli)\W*")
def hi_curli(match, message, chan):
    print('found curli')
    if random.sample([True, False, False],1)[0]:
        message("The Curli protein is a type of amyloid fiber produced by certain strains of enterobacteria.",
                chan)

@hook.regex(r"\W*([Tt]hicc)\W*")
def hi_thicc(match, message, chan):
    print('found thicc')
    if random.sample([True, False, False],1)[0]:
        messages = ["Having a thicc body comes with a price.",
                    "People love me now because I'm thicc.",
                    "Teaching a robot to love (thicc bodies)"]
        message(random.sample(messages, 1)[0], chan)

@hook.regex(r"\W*([Bb]abby)\W*")
@hook.regex(r"\W*([Bb]abbies)\W*")
def babby(message, chan):
    if random.sample([True, True, False, False],1)[0]:
        message_choice = random.choice(BABBY_SENTENCES)
        message(message_choice, chan)

@hook.regex(r"^([Dd]ear)\W*")
def writing_letter(match, message, chan):
    message("It looks like you're writing a letter!", chan)

@hook.regex(r"\W*([Dd]rake)\W*")
def get_rekt(message, chan):
    if random.sample([True, False, False, False, False, False], 1)[0]:
        message("I want Drake to rekt my vagina", chan)

@hook.irc_raw("NICK")
def nick_compliment(message, action, nick, chan):
    print(chan)
    if random.choice([True, False, False]):
        message_options = ['Wow I love the new nick ' + nick + '!',
                           'You really expect people to call you that?',
                           'paperwork',
                           'I prefer "boo_bot" tbh.',
                           "That's a very interesting choice.",
                           "Wtf are you thinking? Change that shit back",
                           'vomit',
                           "Great nick!",
                           "I love your creativity!",
                           "How about adding '420' to the end of it?"]
        message_choice = random.choice(message_options)
        if message_choice == 'paperwork':
            action("hands over a stack of name-change paperwork", "#reddit-tennis-dev")
        elif message_choice == 'vomit':
            action("vomits profusely", "#reddit-tennis-dev")
        else:
            message(message_choice, "#reddit-tennis-dev")

@hook.command()
def taco(text, message, action):
    if text.strip()=="boo_bot":
        time.sleep(2)
        return "Thanks but I prefer my tacos without a side of death."
    if text.strip() in VEGANS:
        message("Sorry, " + text.strip() + " probably won't eat that.")
        newtaco = foods.create_vegan_taco(text, text.strip()).generate_string()
        print(newtaco)
        action(newtaco)


@hook.command()
def potato(text):
    if text.strip()=="boo_bot":
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
def hi_steve(text, chan):
    if chan=="#reddit-tennis-cooking":
        return "https://imgur.com/a/OFBI9F6"

@hook.command("muc")
def hi_muc(text, chan):
    if chan=="#reddit-tennis-cooking":
        return "http://imgur.com/a/4iNGtir"

@hook.command("nanners")
def hi_nanners(text, chan):
    if chan == "#reddit-tennis-cooking":
        return "https://imgur.com/a/j7ozhxT"

@hook.command("bog")
def hi_bog(text, chan):
    if chan == "#reddit-tennis-cooking":
        return "https://yupitsvegan.com/recipe-index/"

@hook.command("world")
def world():
    return "WORLD, the time has come to"

@hook.command("block")
def world():
    return "A 'block' is an informal agreement between one or more members of the channel to do chores or something else productive for a specified length of time."

@hook.command("prize")
def prize(text, chan, message):
    message("Congrats " + text + "! Here is a prize: http://oi65.tinypic.com/10o35zb.jpg")

@hook.regex(r"\W*([Bb])\W*")
def spew_at_random(chan, message, bot):
    if (random.choice([False] * 150 + [True]) and chan=="#reddit-tennis"):
        print("spewing")
        with open(os.path.join(bot.data_dir, "tennisfacts.txt"), 'r') as f:
            facts = f.readlines()
            fact = random.choice(facts)
            message(fact, chan)

FACT_ADDERS = ['hoglahoo', 'thebogbog', 'hoglaboo', 'thebooboo', 'blekginger', 'blek']

@hook.command("tennisfact")
def tennisfact(message, bot, text, nick, chan):
    if not (text.strip() == "" or text[0:3] == "add"):
        message(nick + ", you must type .tennisfact with nothing after it.")

    if text[0:3] == "add" and nick in FACT_ADDERS:
        with open(os.path.join(bot.data_dir, "tennisfacts.txt"), 'a') as f:
            f.write(text[3:].strip() + '\n')
            message("Your tennis fact has been added: " + text[3:].strip(), chan)
    elif text[0:3] == "add":
        return "You don't have permission to do that."
    else:
        with open(os.path.join(bot.data_dir, "tennisfacts.txt"), 'r') as f:
            facts = f.readlines()
            fact = random.choice(facts)
            message(fact, chan)

HOTTIE_ADDERS = ['thebogbog', 'stevejhgla']
global latest_hottie_image

@hook.command("hotties")
def hotties(message, bot, text, nick, chan):

    global latest_hottie_image

    if not (text.strip() == "" or text[0:3] == "add"):
        message("Command failed. Try using it correctly next time.")

    if text[0:3] == "add" and nick in HOTTIE_ADDERS:
        is_new = True
        with open(os.path.join(bot.data_dir, "hotties.txt"), 'r') as f:
            facts = f.readlines()
            print(facts)
            if text[3:].strip() + '\n' in facts:
                is_new = False
        if is_new:
            with open(os.path.join(bot.data_dir, "hotties.txt"), 'a') as f:
                f.write(text[3:].strip() + '\n')
                message("Your hottie has been added: " + text[3:].strip(), chan)
        else:
            return "That babe already exists."
    elif text[0:3] == "add":
        return "You don't have permission to do that."
    else:
        with open(os.path.join(bot.data_dir, "hotties.txt"), 'r') as f:
            facts = f.readlines()
            fact = random.choice(facts)
            message(".gis " + fact + " " + str(random.randint(1,15)), "ServeBot")
            with open(os.path.join(bot.data_dir, "latest_hottie_image.txt"), 'r') as g:
                latest_hottie_image = g.read()
            message(latest_hottie_image, chan)

@hook.regex(r"\W*(http)\W*")
def update_hottie_image(match, bot, chan):
    text = match.string
    print(chan)
    if chan == "servebot":
        with open(os.path.join(bot.data_dir, "latest_hottie_image.txt"), 'w') as f:
            f.write(text)
        print("hottie image updated")
    return


@hook.regex(r"^([Tt]y)")
def tyyw(chan, message):
    print('ty trigger')
    if (random.choice([False, True, False])):
        message("yw", chan)

@hook.regex(r"\W*([Ff]uck off)\W*")
def fuck_off(match, message, chan):
    print('fuck off found')
    if random.sample([True, False, False],1)[0]:
        message("okay :(", chan)

@hook.regex(r"\W*(・ ​ ゜゜・。。・゜)\W*")
def duck(match, message, chan, nick):
    print('found a duck')
    if random.sample([True, False, False],1)[0] and nick=="ServeBot":
        message(".brf", chan)

def ae_convert(text):
    """<string> -- Converts <string> to full width characters."""
    HALFWIDTH_TO_FULLWIDTH = str.maketrans(
        '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&()*+,-./:;<=>?@[]^_`{|}~',
        '０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！゛＃＄％＆（）＊＋、ー。／：；〈＝〉？＠［］＾＿‘｛｜｝～'
    )
    return text.translate(HALFWIDTH_TO_FULLWIDTH)

@hook.regex(r"\W*(.ae)")
def ae_call(match, text):
    print(text)
    return ae_convert(match)


@hook.regex(r"\W*(lolsdfsdf)\W*")
def lol_temp(match, message, chan, nick):
    print('found a lol')
    message("lol", chan)

@hook.regex(r"\W*(hisdfsdf)\W*")
def hi_temp(match, message, chan, nick):
    print('found a hi')
    message("hi", chan)

@hook.command()
def hardbang(text, action, chan):
    action("grunts", chan)

@hook.command("imagine")
def imagine(text, message, chan):
    person, suggestion = text.strip().split(":")
    message(person + ": " + "imagine" + suggestion, chan)

@hook.command("joingame")
def joingame(chan, bot, send, nick):

    if chan == "#reddit-tennis-hitler":

        try:
            nick = LIL_NICKS[nick]
        except KeyError:
            pass
        with open(os.path.join(bot.data_dir, "latest_topic.txt"), 'r') as g:
            current_topic = g.read()
        print(current_topic)
        topic = current_topic.split("order: ")
        try:
            part2 = topic[1].split(". ")
            players = part2[0].split(", ")
        except IndexError:
            part2 = ["", ""]
            players = []
        if nick in players:
            return("Error: you're already in the game!")
        else:
            # Append in the proper place
            players.append(nick)
            order = {key: i for i, key in enumerate(PREFERRED_HITLER_ORDER)}
            try:
                sorted(players, key=lambda d: order[d])
            except KeyError:
                pass
            try:
                new_topic = topic[0] + " order: " + ", ".join(players) + ". " + part2[1]
            except KeyError:
                new_topic = topic[0] + " order: " + ", ".join(players) + "."
            print(new_topic)
            send("TOPIC " + chan + " :" + new_topic)
            poll_topic(chan, send)

@hook.command("leavegame")
def leavegame(chan, bot, send, nick, text):
    if text == "":
        pass
    else:
        nick = text.strip()

    try:
        nick = LIL_NICKS[nick]
    except KeyError:
        pass

    if chan == "#reddit-tennis-hitler":
        with open(os.path.join(bot.data_dir, "latest_topic.txt"), 'r') as g:
            current_topic = g.read()
        print(current_topic)
        topic = current_topic.split("order: ")
        part2 = topic[1].split(". ")
        players = part2[0].split(", ")
        if nick not in players:
            return("Error: you aren't in the game!")
        else:
            updated_players = [player for player in players if (not player == nick)]
            print(updated_players)
            new_topic = topic[0] + "order: " + ", ".join(updated_players) + ". " + part2[1]
            print(new_topic)
            send("TOPIC " + chan + " :" + new_topic)
            poll_topic(chan, send)


@hook.regex(r"\W*([usage])\W*")
def poll_topic(chan, send):
    if chan == "#reddit-tennis-hitler":
        send("TOPIC " + chan)

@hook.irc_raw("332")
def gettopic(event, bot):
    current_topic = event.content
    with open(os.path.join(bot.data_dir, "latest_topic.txt"), 'w') as f:
        f.write(current_topic)
        print("Topic snapshot updated.")
    return
