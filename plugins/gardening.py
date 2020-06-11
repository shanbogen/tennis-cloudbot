import operator
import random
import sqlite3
import os
import datetime

from collections import defaultdict, Counter
from threading import Lock
from time import time, sleep

from cloudbot import hook
from cloudbot.event import EventType
from cloudbot.util.formatting import pluralize_auto

plant_tail = "_.~'~._.~'~. "
plant = ["❀", "✾", "✿", "❀", "❁", "❊"]
plant_noise = [" A seed drops onto the ground."]

HARVESTABLES = ['apple', 'courgette', 'passionfruit', 'cob of corn',
                'common milkweed', 'cumin seed', 'mansplainberry',
                'tomato', 'sprig of thyme', 'soybean', 'kalamata olive',
                'crispiberri']

WILT_RISK_SECONDS = 300
OVERWATER_RESILIENCE = 6
GROWTH_RESISTANCE = 1
FRUIT_RESISTANCE = 4
DROUGHT_RESILIENCE = 4
HARVEST_DIFFICULTY = 1
HIT_RATE = 5

MSG_DELAY = 10
MASK_REQ = 3
scripters = defaultdict(int)
chan_locks = defaultdict(lambda: defaultdict(Lock))
game_status = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))


@hook.event([EventType.message, EventType.action], singlethread=True)
def incrementMsgCounter(event, conn):
    """Increment the number of messages said in an active game channel. Also keep track of the unique masks that are speaking."""
    global game_status
    if event.chan in ["#reddit-tennis-dev"]:
        if game_status[event.chan]['game_on'] == 1 and game_status[event.chan]['plant_status'] == 0:
            game_status[event.chan]['messages'] += 1
            if event.host not in game_status[event.chan]['masks']:
                game_status[event.chan]['masks'].append(event.host)
    return

# TODO: save game state to file upon quit/reload
@hook.on_start()
def reload_game(bot):

    global game_status

    # TODO: loop through all channels if applicable
    chan = "#reddit-tennis-dev"

    set_planttime(chan)
    game_status[chan]['game_on'] = 1
    game_status[chan]['plant_status'] = 0

    return


@hook.command("startgarden", autohelp=False)
def startgarden(chan, message):
    """- This command starts a gardening game in your channel, to stop the hunt use .stopgarden"""
    global game_status
    if chan not in ["#reddit-tennis-dev"]:
        return
    check = game_status[chan]['game_on']
    if check:
        return "there is already a game running in {}.".format(chan)

    set_planttime(chan)
    game_status[chan]['game_on'] = 1
    message(
        "Eureka! A plot of land is ripe for gardening. If you spot a seed, gather and plant it with .collect. Don't forget to water your plants with .water, " + \
        "befriend lots of ducks to help you fertilize them, and harvest the plant when it's ready!",
        chan)


def set_planttime(chan):
    global game_status
    game_status[chan]['next_plant_time'] = random.randint(int(time()) + 480, int(time()) + 3600)
    game_status[chan]['plant_status'] = 0
    # let's also reset the number of messages said and the list of masks that have spoken.
    game_status[chan]['messages'] = 0
    game_status[chan]['masks'] = []
    return


@hook.command("stopgarden", autohelp=False)
def stopgarden(db, chan, conn):
    """- This command stops the plant hunt in your channel. Scores will be preserved"""
    global game_status
    if chan not in ["#reddit-tennis-dev"]:
        return
    if game_status[chan]['game_on']:
        game_status[chan]['game_on'] = 0
        return "the gardening game has been stopped."
    else:
        return "There is no gardening game running in {}.".format(chan)


@hook.command("gardenkick", permissions=["chanop", "op", "botcontrol"])
def no_plant_kick(db, text, chan, conn, notice_doc):
    """<enable|disable> - If the bot has OP or half-op in the channel you can specify .plantkick enable|disable so that people are kicked for shooting or befriending a non-existent goose. Default is off."""
    global game_status
    if chan in ["#reddit-tennis-dev"]:
        return
    if text.lower() == 'enable':
        return "users will now be kicked for trying to acquire non-existent seeds. The bot needs to have appropriate flags to be able to kick users for this to work."
    elif text.lower() == 'disable':
        return "kicking for non-existent seeds has been disabled."
    else:
        notice_doc()
        return

def generate_seed():
    """Try and randomize the plant message so people can't highlight on it/script against it."""
    rt = random.randint(1, len(plant_tail) - 1)
    dtail = plant_tail[:rt] + u' \u200b ' + plant_tail[rt:]
    dbody = random.choice(plant)
    dnoise = random.choice(plant_noise)
    rn = random.randint(1, len(dnoise) - 1)
    dnoise = dnoise[:rn] + u'\u200b' + dnoise[rn:]
    return dtail, dbody, dnoise


@hook.command("seedspawn")
def seedspawn(message, chan):
    global game_status
    active = game_status[chan]['game_on']
    plant_status = game_status[chan]['plant_status']
    if active == 0:
        startgarden(chan, message)
    if active == 1 and plant_status == 0:
        # deploy a plant to channel
        game_status[chan]['plant_status'] = 1
        game_status[chan]['plant_time'] = time()
        dtail, dbody, dnoise = generate_seed()
        message("{}{}{}".format(dtail, dbody, dnoise), chan)
    else:
        print('Seed tried to spawn when theres already an active seed')

@hook.periodic(11, initial_interval=11)
def deploy_seed(bot, message):
    global game_status
    for chan in game_status:
        active = game_status[chan]['game_on']
        plant_status = game_status[chan]['plant_status']
        next_plant = game_status[chan]['next_plant_time']
        chan_messages = game_status[chan]['messages']
        chan_masks = game_status[chan]['masks']
        if active == 1 and plant_status == 0 and next_plant <= time() and chan_messages >= MSG_DELAY and len(
            chan_masks) >= MASK_REQ:
            # deploy a plant to channel
            game_status[chan]['plant_status'] = 1
            game_status[chan]['plant_time'] = time()
            dtail, dbody, dnoise = generate_seed()
            message("{}{}{}".format(dtail, dbody, dnoise), chan)
        continue


def attack(event, nick, chan, message, notice, bot):
    global game_status, scripters, conn
    if chan not in ["#reddit-tennis-dev"]:
        return

    status = game_status[chan]

    out = ""
    miss = [
            "The seed rolled under your refrigerator.",
            "Whoops, you grabbed a nearby piece of lint instead of the seed.",
            "Your thick tofurky fingers couldn't successfully pluck the seed from the ground.",
        ]
    no_plant = "You tried to pick up a seed that doesn't exist. Go find something better to do."
    msg = "{} you grabbed a seed in {:.3f} seconds! You have {} seedlings and plants in your garden."
    scripter_msg = "You tried picking up that seed in {:.3f} seconds, that's mighty fast. Are you sure you aren't a script? Take a 2 hour cool down."
    attack_type = "friend"

    if not status['game_on']:
        return "There is no gardening game right now. Use .startgarden to start a game."
    elif status['plant_status'] == 1:
        status['shoot_time'] = time()
        deploy = status['plant_time']
        shoot = status['shoot_time']
        if nick.lower() in scripters:
            if scripters[nick.lower()] > shoot:
                notice(
                    "You are in a cool down period, you can try again in {:.3f} seconds.".format(
                        scripters[nick.lower()] - shoot
                    )
                )
                return

        attack_success = random.choice([True] * HIT_RATE + [False])
        if not attack_success:
            out = random.choice(miss) + " You can try again in 7 seconds."
            scripters[nick.lower()] = shoot + 7
            return out

        if shoot - deploy < 1:
            out += scripter_msg.format(shoot - deploy)
            scripters[nick.lower()] = shoot + 7200
            if not random.random() <= 0.05:
                return random.choice(miss) + " " + out
            else:
                message(out)

        status['plant_status'] = 2
        try:
            args = {
                attack_type: 1
            }

            conn = sqlite3.connect(os.path.join(bot.data_dir, "gardening.db"))
            c = conn.cursor()
            t = (nick,)
            c.execute('SELECT * FROM gardener WHERE nick=?', t)
            if c.fetchone() is None:
                c.execute("INSERT INTO gardener(nick) VALUES (?)", t)
                conn.commit()

            planttype = random.choice(HARVESTABLES)
            c.execute('SELECT * FROM gardener WHERE nick=?', t)
            gardener_id = c.fetchone()[0]
            now = datetime.datetime.now()

            c.execute("INSERT INTO plant(stage, waterlevel, fruit, harvested, lastwatered, status, gardenerID, fruittype) VALUES (0, 0, 0, 0, ?, 'alive', ?, ?)",
                      (now, gardener_id, random.choice(HARVESTABLES)))
            conn.commit()

            c.execute("SELECT * FROM plant WHERE gardenerID=? AND status == 'alive'", (gardener_id,))
            score = len(c.fetchall())
            game_status[chan]['plant_status'] = 0
        except Exception:
            status['plant_status'] = 1
            event.reply("An unknown error has occurred.")
            raise

        message(msg.format(nick, shoot - deploy, pluralize_auto(score, "plant"), chan))
        set_planttime(chan)
    else:
        message(no_plant, chan)


@hook.command("collect", autohelp=False)
def collect(nick, chan, message, db, conn, notice, event, bot):
    """- when there is a seed on the loose use this command to pick it up."""
    return attack(event, nick, chan, message, notice, bot)


# TODO: functionality to water someone else's plants
# TODO: random seeds should appear
# TODO: plants should dry out over time and die regardless of .water use


def smart_truncate(content, length=320, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return content[:length].rsplit(' • ', 1)[0] + suffix


@hook.command("gardeners", autohelp=False)
def harvesters(text, chan, conn, db):
    """[{global|average}] - Prints a list of the top harvesters in the channel, if 'global' is specified all channels in the database are included."""
    if chan in ["#reddit-tennis-dev"]:
        return
    friends = defaultdict(int)
    chancount = defaultdict(int)
    out = "plant harvest scores in {}: ".format(chan)
    # TODO: call to db to get harvest scores
    scores = None
    if scores:
        for row in scores:
            if row[1] == 0:
                continue
            friends[row[0]] += row[1]
        else:
            return "it appears no one has harvested any bounty yet."

    topfriends = sorted(friends.items(), key=operator.itemgetter(1), reverse=True)
    out += ' • '.join(["{}: {:,}".format('\x02' + k[:1] + u'\u200b' + k[1:] + '\x02', v) for k, v in topfriends])
    out = smart_truncate(out)
    return out


@hook.command("plantforgive")
def plantforgive(text, nick):
    """<nick> - Allows people to be removed from the mandatory cooldown period."""
    global scripters
    if nick != "thebogbog":
        return "You don't have permission to do that."
    if text.lower() in scripters and scripters[text.lower()] > time():
        scripters[text.lower()] = 0
        return "{} has been removed from the mandatory cooldown period.".format(text)
    else:
        return "I couldn't find anyone banned from the farm by that nick"


@hook.command("plants", autohelp=False)
def plants_user(text, nick, chan, bot, message):
    """<nick> - Prints a users plant stats. If no nick is input it will check the calling username."""
    name = nick.lower()
    if text:
        name = text.split()[0].lower()

    conn = sqlite3.connect(os.path.join(bot.data_dir, "gardening.db"))
    c = conn.cursor()

    c.execute('SELECT * FROM gardener WHERE nick=?', (name,))
    results = c.fetchone()
    if results is None:
        return("It seems that " + name + " hasn't started their garden yet.")
    gardener_id = results[0]

    # Get all plants for a gardener
    c.execute("SELECT * FROM plant WHERE gardenerID=? AND status == 'alive' AND stage > 0", (gardener_id,))
    results = c.fetchall()
    plants = len(results)

    c.execute("SELECT * FROM plant WHERE gardenerID=? AND status == 'alive' AND stage == 0", (gardener_id,))
    results = c.fetchall()
    seedlings = len(results)

    c.execute("SELECT fruit FROM plant WHERE gardenerID=? AND status == 'alive' AND fruit > 0", (gardener_id,))
    results = c.fetchall()
    fruits = sum([plant[0] for plant in results])

    if text:
        message(name + " has " + str(seedlings) + " seedlings, " + str(plants) + " plants in their garden and "
                + str(fruits) + " bounty available to harvest.")
    else:
        message(nick + ", you have " + str(seedlings) + " seedlings, " + str(plants) + " plants in your garden and "
                + str(fruits) + " bounty available to harvest.")

@hook.command("crops", autohelp=False)
def crops_user(text, nick, chan, bot, message):
    """<nick> - Prints a users plant stats. If no nick is input it will check the calling username."""
    name = nick.lower()
    if text:
        name = text.split()[0].lower()

    conn = sqlite3.connect(os.path.join(bot.data_dir, "gardening.db"))
    c = conn.cursor()

    c.execute('SELECT * FROM gardener WHERE nick=?', (name,))
    results = c.fetchone()
    if results is None:
        return "It seems that " + name + " hasn't started their garden yet."
    gardener_id = results[0]

    # Get all plants for a gardener
    c.execute("SELECT sum(harvested), fruittype FROM plant WHERE gardenerID=? AND harvested > 0 group by fruittype", (gardener_id,))
    results = c.fetchall()
    if results:

        harvest_counts = [plant[0] for plant in results]
        harvest_total = sum(harvest_counts)
        fruit_types = [plant[1] for plant in results]

        fruitcounts = ''
        fruit_type_totals = dict(zip(fruit_types, harvest_counts))
        for key, value in fruit_type_totals.items():
            fruitcounts += str(value) + ' ' + str(key) + ' '

        return "{} has harvested a total of {} edible delicacies: {}".format(name, harvest_total, fruitcounts)
    else:
        return "It seems that {} hasn't harvested anything yet.".format(name)


@hook.command('water', autohelp=False)
def water(nick, chan, bot, message):

    conn = sqlite3.connect(os.path.join(bot.data_dir, "gardening.db"))
    c = conn.cursor()
    c.execute('SELECT * FROM gardener WHERE nick=?', (nick,))
    results = c.fetchone()
    if results is None:
        return ("It seems that you haven't started your garden yet.")
    gardener_id = results[0]

    now = datetime.datetime.now()

    # TODO: decrement the water level of all plants based on how much time has passed.
    # TODO: make plants more likely to die if their water levels are lower, instead of just a binary.

    c.execute("SELECT plantID FROM plant WHERE gardenerID=? AND status == 'alive'",
              (gardener_id,))
    results = c.fetchall()
    if not results:
        return ("It seems you are a failed gardener with no live plants available to water. Sorry!")

    c.execute("SELECT plantID, ((julianday('now') - julianday(lastwatered))) as age FROM plant WHERE gardenerID=? AND status == 'alive' AND "
              "waterlevel < 2 AND ((julianday('now') - julianday(lastwatered))) > ?", (gardener_id, WILT_RISK_SECONDS))
    results = c.fetchall()
    print([plant[1] for plant in results])
    if results:
        num_dried = len(results)
        num_to_dispose = random.choice([0] * DROUGHT_RESILIENCE + [random.randint(1, num_dried)])
        if num_to_dispose == 0:
            mtext = "You discover that you were neglecting {} of your plants, but thankfully they all survived. ".format(num_dried)
        else:
            disposed_ids = random.choices([plantid[0] for plantid in results], k=num_to_dispose)
            disposed_ids = [(plantid,) for plantid in disposed_ids]
            c.executemany("UPDATE plant SET status = 'dead' WHERE plantID = ?",
                          disposed_ids)
            conn.commit()
            return("Upon getting to the garden you discover that you neglected {} of your plants, and {} of them had to be thrown away. ".
                   format(num_dried,num_to_dispose) +
                   "You'll have to come back later.")

    # Water all plants
    c.execute("UPDATE plant SET waterlevel = waterlevel + 1 WHERE gardenerID=? AND status == 'alive'", (gardener_id,))
    conn.commit()
    mtext = "You watered your plants. "

    # Check for plants that are over-watered
    c.execute("SELECT plantID FROM plant WHERE gardenerID=? AND status == 'alive' AND waterlevel > 6", (gardener_id,))
    results = c.fetchall()
    if results:
        num_overwatered = len(results)
        num_to_kill = random.choice([0] * OVERWATER_RESILIENCE + [random.randint(1, num_overwatered)])
        if num_to_kill == 0:
            mtext = "You overwatered {} of your plants, but thankfully they all survived. ".format(num_overwatered)
        else:
            overwatered_ids = random.choices([plantid[0] for plantid in results], k=num_to_kill)
            overwatered_ids = [(plantid,) for plantid in overwatered_ids]
            c.executemany("UPDATE plant SET status = 'dead' WHERE plantID = ?",
                      overwatered_ids)
            conn.commit()
            mtext = "You overwatered {} of your plants, and {} of them died. ".format(num_overwatered,
                                                                                                         num_to_kill)

    # Check for plants that are watered enough to stage up and not yet at fruiting stage
    c.execute("SELECT * FROM plant WHERE gardenerID=? AND status == 'alive' AND waterlevel > 2 AND stage < 2", (gardener_id,))
    results = c.fetchall()
    if results:
        num_eligible = len(results)
        num_leveled = random.choice([0] * GROWTH_RESISTANCE + [random.randint(1, num_eligible)])
        if num_leveled > 0:
            leveled_ids = random.choices([plantid[0] for plantid in results], k=num_leveled)
            leveled_ids = [(plantid,) for plantid in leveled_ids]
            c.executemany("UPDATE plant SET stage = stage + 1 WHERE plantID = ?",
                          leveled_ids)
            c.executemany("UPDATE plant SET waterlevel = waterlevel - 1 WHERE plantID = ?",
                          leveled_ids)
            conn.commit()
            mtext = mtext + "{} of the plants looked immediately taller and sturdier. ".format(num_leveled)

    # Check for plants that are watered enough and staged enough to yield fruit
    c.execute("SELECT plantid FROM plant WHERE gardenerID=? AND status == 'alive' AND waterlevel > 3 AND stage > 1", (gardener_id,))
    results = c.fetchall()
    if results:
        num_eligible = len(results)
        num_fruiting = random.choice([0] * FRUIT_RESISTANCE + [random.randint(1, num_eligible)])
        if num_fruiting > 0:
            fruiting_ids = random.choices([plantid[0] for plantid in results], k=num_fruiting)
            fruiting_ids_formatted = [(plantid,) for plantid in fruiting_ids]
            c.executemany("UPDATE plant SET fruit = fruit + 1 WHERE plantID = ?",
                          fruiting_ids_formatted)
            c.executemany("UPDATE plant SET waterlevel = waterlevel - 1 WHERE plantID = ?",
                          fruiting_ids_formatted)
            conn.commit()

            c.execute(
                "SELECT fruittype, count(*) FROM plant WHERE plantid IN (%s) GROUP BY fruittype" % ','.join('?'*len(fruiting_ids)), fruiting_ids)
            results = c.fetchall()
            results = [fruit[0] for fruit in results]
            fruitcounts = ''
            for key, value in Counter(results).items():
                fruitcounts += str(value) + ' ' + str(key) + ' '

            mtext = mtext + "{} of the mature plants produced {}!".\
                format(num_fruiting, fruitcounts)

    return(mtext)

@hook.command("bestplant", autohelp=False)
def best_plant(bot, message, chan):
    """<nick> - Prints a users plant stats. If no nick is input it will check the calling username."""

    conn = sqlite3.connect(os.path.join(bot.data_dir, "gardening.db"))
    c = conn.cursor()

    # Get the owner and age of the best plants
    c.execute("SELECT stage, gardenerID FROM plant WHERE status == 'alive' AND stage = (SELECT MAX(stage) FROM plant WHERE status == 'alive')")
    results = c.fetchone()
    stage = results[0]
    gardener_id = results[1]

    c.execute('SELECT nick FROM gardener WHERE gardenerID=?', (gardener_id,))
    nick = c.fetchone()[0]

    message("{} currently has the best plant, lovingly watering it to grow larger {} times!".format(nick, stage), chan)

@hook.command("worstgardener", autohelp=False)
def worst_gardener(bot, message, chan):
    """<nick> - Prints a users plant stats. If no nick is input it will check the calling username."""

    conn = sqlite3.connect(os.path.join(bot.data_dir, "gardening.db"))
    c = conn.cursor()

    # Get the owner and age of the best plants
    c.execute("SELECT gardenerID, count(*) AS finalcount FROM plant WHERE status == 'dead' GROUP BY gardenerID ORDER BY count(*) DESC")
    results = c.fetchone()
    gardener_id = results[0]
    num_dead = results[1]

    c.execute('SELECT nick FROM gardener WHERE gardenerID=?', (gardener_id,))
    nick = c.fetchone()[0]

    message("{} is currently the worst gardener, with {} total plants killed due to abuse and neglect. ".format(nick, num_dead), chan)

@hook.command("bestgardener", autohelp=False)
def best_gardener(bot, message, chan):
    """<nick> - Prints a users plant stats. If no nick is input it will check the calling username."""

    conn = sqlite3.connect(os.path.join(bot.data_dir, "gardening.db"))
    c = conn.cursor()

    # Get the owner and age of the best plants
    c.execute("SELECT gardenerID, count(*) AS finalcount FROM plant WHERE status != 'dead' AND stage > 0 GROUP BY gardenerID ORDER BY count(*) DESC")
    results = c.fetchone()
    gardener_id = results[0]
    num_live = results[1]

    c.execute('SELECT nick FROM gardener WHERE gardenerID=?', (gardener_id,))
    nick = c.fetchone()[0]

    message("{} is currently the best gardener, with {} total live plants. ".format(nick, num_live), chan)

@hook.command("harvest", autohelp=False)
def harvest(bot, message, chan, nick):
    """<nick> - Prints a users plant stats. If no nick is input it will check the calling username."""

    conn = sqlite3.connect(os.path.join(bot.data_dir, "gardening.db"))
    c = conn.cursor()
    c.execute('SELECT * FROM gardener WHERE nick=?', (nick,))
    results = c.fetchone()
    if results is None:
        return ("It seems that you haven't started your garden yet.")
    gardener_id = results[0]

    c.execute("SELECT plantID, fruit FROM plant WHERE gardenerID=? AND status == 'alive' AND fruit > 0",
              (gardener_id,))
    results = c.fetchall()
    if results:
        num_fruiting_plants = len(results)
        num_fruit = sum([plant[1] for plant in results])

        success = random.choice([False] * HARVEST_DIFFICULTY + [True])
        if success:

            harvested_ids = [plant[0] for plant in results]
            harvested_ids_formatted = [(item,) for item in harvested_ids]

            c.executemany("UPDATE plant SET fruit = fruit - 1 WHERE plantID = ?",
                          harvested_ids_formatted)
            c.executemany("UPDATE plant SET harvested = harvested + 1 WHERE plantID = ?",
                          harvested_ids_formatted)
            conn.commit()

            c.execute(
                "SELECT fruittype FROM plant WHERE plantid IN (%s)" % ','.join('?' * len(harvested_ids)), harvested_ids)
            results = c.fetchall()
            results = [fruit[0] for fruit in results]
            fruitcounts = ''
            for key, value in Counter(results).items():
                fruitcounts += str(value) + ' ' + str(key) + ' '

            return (
                    "In your jaunt through the garden you successfully harvested item(s) out of a possible {} items on"
                    " {} plants, namely, {}".format(num_fruit, num_fruiting_plants, fruitcounts))
        else:
            return("Plants have feelings too, and they resisted your inappropriate harvest attempt.")
    else:
        return("You don't have any plants with harvestable fruit. Be patient and try again later.")

@hook.command("bestfarmer", autohelp=False)
def best_farmer(bot, message, chan):
    """<nick> - Prints a users plant stats. If no nick is input it will check the calling username."""

    conn = sqlite3.connect(os.path.join(bot.data_dir, "gardening.db"))
    c = conn.cursor()

    # Get the owner and age of the best plants
    c.execute("SELECT gardenerID, sum(harvested) as result FROM plant group by gardenerID order by result desc")
    results = c.fetchone()
    harvests = results[1]
    gardener_id = results[0]

    c.execute('SELECT nick FROM gardener WHERE gardenerID=?', (gardener_id,))
    nick = c.fetchone()[0]

    message("{} is currently the best farmer, with {} total harvests".format(nick, harvests), chan)
