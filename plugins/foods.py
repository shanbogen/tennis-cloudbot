import asyncio
import json

import codecs
import os
import random
import re

from cloudbot import hook
from cloudbot.util import textgen

nick_re = re.compile("^[A-Za-z0-9_|.\-\]\[\{\}]*$", re.I)

potatoes = ['AC Belmont', 'AC Blue Pride', 'AC Brador', 'AC Chaleur', 'AC Domino', 'AC Dubuc', 'AC Glacier Chip',
            'AC Maple Gold', 'AC Novachip', 'AC Peregrine Red', 'AC Ptarmigan', 'AC Red Island', 'AC Saguenor',
            'AC Stampede Russet', 'AC Sunbury', 'Abeille', 'Abnaki', 'Acadia', 'Acadia Russet', 'Accent',
            'Adirondack Blue', 'Adirondack Red', 'Adora', 'Agria', 'All Blue', 'All Red', 'Alpha', 'Alta Russet',
            'Alturas Russet', 'Amandine', 'Amisk', 'Andover', 'Anoka', 'Anson', 'Aquilon', 'Arran Consul', 'Asterix',
            'Atlantic', 'Austrian Crescent', 'Avalanche', 'Banana', 'Bannock Russet', 'Batoche', 'BeRus',
            'Belle De Fonteney', 'Belleisle', 'Bintje', 'Blossom', 'Blue Christie', 'Blue Mac', 'Brigus',
            'Brise du Nord', 'Butte', 'Butterfinger', 'Caesar', 'CalWhite', 'CalRed', 'Caribe', 'Carlingford',
            'Carlton', 'Carola', 'Cascade', 'Castile', 'Centennial Russet', 'Century Russet', 'Charlotte', 'Cherie',
            'Cherokee', 'Cherry Red', 'Chieftain', 'Chipeta', 'Coastal Russet', 'Colorado Rose', 'Concurrent',
            'Conestoga', 'Cowhorn', 'Crestone Russet', 'Crispin', 'Cupids', 'Daisy Gold', 'Dakota Pearl', 'Defender',
            'Delikat', 'Denali', 'Desiree', 'Divina', 'Dundrod', 'Durango Red', 'Early Rose', 'Elba', 'Envol',
            'Epicure', 'Eramosa', 'Estima', 'Eva', 'Fabula', 'Fambo', 'Fremont Russet', 'French Fingerling',
            'Frontier Russet', 'Fundy', 'Garnet Chile', 'Gem Russet', 'GemStar Russet', 'Gemchip', 'German Butterball',
            'Gigant', 'Goldrush', 'Granola', 'Green Mountain', 'Haida', 'Hertha', 'Hilite Russet', 'Huckleberry',
            'Hunter', 'Huron', 'IdaRose', 'Innovator', 'Irish Cobbler', 'Island Sunshine', 'Ivory Crisp',
            'Jacqueline Lee', 'Jemseg', 'Kanona', 'Katahdin', 'Kennebec', "Kerr's Pink", 'Keswick', 'Keuka Gold',
            'Keystone Russet', 'King Edward VII', 'Kipfel', 'Klamath Russet', 'Krantz', 'LaRatte', 'Lady Rosetta',
            'Latona', 'Lemhi Russet', 'Liberator', 'Lili', 'MaineChip', 'Marfona', 'Maris Bard', 'Maris Piper',
            'Matilda', 'Mazama', 'McIntyre', 'Michigan Purple', 'Millenium Russet', 'Mirton Pearl', 'Modoc', 'Mondial',
            'Monona', 'Morene', 'Morning Gold', 'Mouraska', 'Navan', 'Nicola', 'Nipigon', 'Niska', 'Nooksack',
            'NorValley', 'Norchip', 'Nordonna', 'Norgold Russet', 'Norking Russet', 'Norland', 'Norwis', 'Obelix',
            'Ozette', 'Peanut', 'Penta', 'Peribonka', 'Peruvian Purple', 'Pike', 'Pink Pearl', 'Prospect', 'Pungo',
            'Purple Majesty', 'Purple Viking', 'Ranger Russet', 'Reba', 'Red Cloud', 'Red Gold', 'Red La Soda',
            'Red Pontiac', 'Red Ruby', 'Red Thumb', 'Redsen', 'Rocket', 'Rose Finn Apple', 'Rose Gold', 'Roselys',
            'Rote Erstling', 'Ruby Crescent', 'Russet Burbank', 'Russet Legend', 'Russet Norkotah', 'Russet Nugget',
            'Russian Banana', 'Saginaw Gold', 'Sangre', 'Satina', 'Saxon', 'Sebago', 'Shepody', 'Sierra',
            'Silverton Russet', 'Simcoe', 'Snowden', 'Spunta', "St. John's", 'Summit Russet', 'Sunrise', 'Superior',
            'Symfonia', 'Tolaas', 'Trent', 'True Blue', 'Ulla', 'Umatilla Russet', 'Valisa', 'Van Gogh', 'Viking',
            'Wallowa Russet', 'Warba', 'Western Russet', 'White Rose', 'Willamette', 'Winema', 'Yellow Finn',
            'Yukon Gold']


def is_valid(target):
    """ Checks if a string is a valid IRC nick. """
    if nick_re.match(target):
        return True
    else:
        return False


@hook.on_start()
def load_foods(bot):
    """
    :type bot: cloudbot.bot.CloudBot
    """
    global sandwich_data, taco_data, buddhabowl_data, sundae_data, burger_data, pizza_data

    with codecs.open(os.path.join(bot.data_dir, "sandwich.json"), encoding="utf-8") as f:
        sandwich_data = json.load(f)

    with codecs.open(os.path.join(bot.data_dir, "taco.json"), encoding="utf-8") as f:
        taco_data = json.load(f)

    with codecs.open(os.path.join(bot.data_dir, "buddhabowl.json"), encoding="utf-8") as f:
        buddhabowl_data = json.load(f)

    with codecs.open(os.path.join(bot.data_dir, "sundae.json"), encoding="utf-8") as f:
        sundae_data = json.load(f)

    with codecs.open(os.path.join(bot.data_dir, "burger.json"), encoding="utf-8") as f:
        burger_data = json.load(f)

    with codecs.open(os.path.join(bot.data_dir, "pizza.json"), encoding="utf-8") as f:
        pizza_data = json.load(f)


@asyncio.coroutine
@hook.command
def veganpotato(text, action):
    """<user> - makes <user> a tasty little potato"""
    user = text.strip()

    if not is_valid(user):
        return "I can't give a potato to that user."

    potato_type = random.choice(potatoes)
    size = random.choice(['small', 'little', 'mid-sized', 'medium-sized', 'large', 'gigantic'])
    flavor = random.choice(['tasty', 'delectable', 'delicious', 'yummy', 'toothsome', 'scrumptious', 'luscious'])
    method = random.choice(['bakes', 'fries', 'boils', 'roasts'])
    side_dish = random.choice(['kale salad', 'dollop of cashew cream', 'piece of tempeh', 'bowl of BBQ jackfruit'])

    action("{} a {} {} {} potato for {} and serves it with a small {}!".format(method, flavor, size, potato_type, user,
                                                                               side_dish))


@asyncio.coroutine
@hook.command
def vegansandwich(text, action):
    """<user> - give a tasty sandwich to <user>"""
    user = text.strip()

    if not is_valid(user):
        return "I can't give a sandwich to that user."

    generator = textgen.TextGenerator(sandwich_data["templates"], sandwich_data["parts"],
                                      variables={"user": user})

    # act out the message
    action(generator.generate_string())

@asyncio.coroutine
@hook.command
def buddhabowl(text, action):
    """<user> - give a health-promoting buddha bowl to <user>"""
    user = text.strip()

    if not is_valid(user):
        return "I can't give a buddha bowl to that user."

    generator = textgen.TextGenerator(buddhabowl_data["templates"], buddhabowl_data["parts"],
                                      variables={"user": user})

    # act out the message
    action(generator.generate_string())


@asyncio.coroutine
@hook.command
def vegantaco(text, action, chan):
    """<user> - give a taco to <user>"""
    user = text.strip()

    if not is_valid(user):
        return "I can't give a taco to that user."

    generator = create_vegan_taco(text, user)
    # act out the message
    action(generator.generate_string())

def create_vegan_taco(text, user):
    return textgen.TextGenerator(taco_data["templates"], taco_data["parts"],
                                      variables={"user": user})

@asyncio.coroutine
@hook.command
def tacosalad(text, action, message):
    """<user> - give a taco to <user>"""
    user = text.strip()

    if not is_valid(user):
        return "I can't give a taco to that user."

    generator = create_vegan_taco(text, user)
    # act out the message
    action(generator.generate_string())
    message("Hmm, actually you're looking a little chubby.")
    action("removes " + user + "'s taco shell and sprinkles some lettuce.")

@asyncio.coroutine
@hook.command
def veganpizza(text, action):
    """<user> - give a pizza to <user>"""
    user = text.strip()

    if not is_valid(user):
        return "I can't give a pizza to that user."

    generator = textgen.TextGenerator(pizza_data["templates"], pizza_data["parts"],
                                      variables={"user": user})

    # act out the message
    action(generator.generate_string())


@asyncio.coroutine
@hook.command
def sundae(text, action):
    """<user> - give a sundae to <user>"""
    user = text.strip()

    if not is_valid(user):
        return "I can't give a sundae to that user."

    generator = textgen.TextGenerator(sundae_data["templates"], sundae_data["parts"],
                                      variables={"user": user})

    # act out the message
    action(generator.generate_string())

@asyncio.coroutine
@hook.command('veggieburger', 'veganburger')
def veggieburger(text, action):
    """<user> - give a burger to <user>"""
    user = text.strip()

    if not is_valid(user):
        return "I can't give a burger to that user."

    generator = textgen.TextGenerator(burger_data["templates"], burger_data["parts"],
                                      variables={"user": user})

    # act out the message
    action(generator.generate_string())
