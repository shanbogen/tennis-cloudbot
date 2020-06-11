"""
recipe.py

Provides commands for searching recipes. Also has a number of commands for returning random recipes
in multiple formats.

Created By:
    - Luke Rogers <https://github.com/lukeroge>

License:
    GPL v3
"""



import requests
import bs4
import re
import unicodedata

from cloudbot import hook

WTA_LIVE_URL = "https://live-tennis.eu/en/wta-live-ranking"
ATP_LIVE_URL = "https://live-tennis.eu/en/atp-live-ranking"
WTA_URL = "https://live-tennis.eu/en/official-wta-ranking"
ATP_URL = "https://live-tennis.eu/en/official-atp-ranking"

CHARACTER_MAPPING: {'í': 'i',
                    'š': 's',
                    'á': 'a'}


def get_rank(text_input, rtype='live', mode='current'):

    if text_input:

        if text_input.lower() == "dave" or text_input.lower() == "atp dave":
            text_input = 'atp novak'

        if text_input.lower() == "ddr" or text_input.lower() == "atp ddr":
            text_input = 'atp nishikori'

        if text_input.lower() == "waitress" or text_input.lower() == "wta waitress":
            text_input = 'wta Timea Bacsinszky'

        if text_input.lower() == "inky" or text_input.lower() == "wta inky":
            text_input = 'wta karolina pliskova'

        if text_input.lower() == "shoulders" or text_input.lower() == "wta shoulders":
            text_input = 'wta Sakkari'

        if text_input.lower() == "eyebrow" or text_input.lower() == "atp eyebrow":
            text_input = 'atp Cilic'

        if text_input.lower() == "fed" or text_input.lower() == "atp fed":
            text_input = 'atp federer'

        if text_input.lower() == "atp goat":
            text_input = 'atp federer'

        if text_input.lower() == "wta goat":
            text_input = 'wta serena williams'

        if text_input.lower() == "sabali" or text_input.lower() == "wta sabali":
            text_input = 'wta Sakkari'

        try:
            input_split = text_input.split(" ", 1)
            category = input_split[0]
            text = input_split[1]
        except IndexError as e:
            return "Please use the format 'rank {atp|wta} {player|number}'"

        if category.lower() == "atp":
            if rtype == 'live':
                url = ATP_LIVE_URL
            else:
                url = ATP_URL
        elif category.lower() == "wta":
            if rtype == 'live':
                url = WTA_LIVE_URL
            else:
                url = WTA_URL
        else:
            return "Please use the format 'rank {atp|wta} {player|number}'"

        try:
            request = requests.get(url)
            request.raise_for_status()
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
            return "Error accessing website"

        result = bs4.BeautifulSoup(request.content, 'html.parser')

        # Integer ranking-based
        try:

            rank = int(text)

            try:
                results = result.find('tbody').find_all('tr', {'class': True})
            except AttributeError as e:
                return "Error parsing rank table from website"

            loc = (rank - 1)

            if rtype == 'live':
                playerwidth = '150'
            else:
                playerwidth = '170'

            name = results[loc].find('td', {'width' : playerwidth})
            print(name)
            try:
                name_text = name.text
            except AttributeError as e:
                return "Something is fucked up, sry"

            if ("<p" in str(name)):
                print('hi')
                try:
                    results2 = result.find('tbody')
                    results2_int = unicodedata.normalize('NFKD', str(results)).encode('ascii', 'ignore')
                    results2_enc = bs4.BeautifulSoup(results2_int)

                except AttributeError as e:
                    return "Error parsing rank table from website"

                if category.lower() == 'wta':
                    bart_person = results2_enc.find(string=re.compile("Barty",
                                                            re.IGNORECASE))
                elif category.lower() == 'atp':
                    bart_person = results2_enc.find(string=re.compile("Zverev",
                                                                      re.IGNORECASE))
                bart_rank = int(bart_person.parent.parent.parent.find('td', {'width': '20'}).text) - 1
                bart_name = str(results[bart_rank].find('td', {'width' : playerwidth}))
                bart_class_1 = bart_name.split("Ashleigh Barty")[0]
                bart_class_2 = bart_class_1.split("class=\"")[1].split("\">")[0]
                correct_class = bart_class_2

                print(correct_class)
                selected_name = name.find('p', {'class' : correct_class})
                name_text = selected_name.text

            return "#" + str(rank) + ": " + name_text.strip()

        # Name-based
        except ValueError:

            try:
                results = result.find('tbody')
                results_int = unicodedata.normalize('NFKD', str(results)).encode('ascii', 'ignore')
                results_enc = bs4.BeautifulSoup(results_int)

            except AttributeError as e:
                return "Error parsing rank table from website"

            person = results_enc.find(string=re.compile(text,
                                                  re.IGNORECASE))
            try:
                if mode=='career-high':
                    rank = person.parent.parent.find_all('td', {'width':"20"})[1].text
                    if 'CH' in rank:
                        rank = person.parent.parent.find_all('td', {'width': "20"})[0].text
                else:
                    print(person.parent.parent.parent)
                    rank = person.parent.parent.find('td', {'width': '20'}).text
            except AttributeError as e:
                try:
                    rank = person.parent.parent.parent.find('td', {'width': '20'}).text
                except AttributeError as e:
                    return "Player not found"

            if mode != 'career-high':
                return "#" + rank.strip() + ": " + person.strip()
            else:
                return 'Career high - ' + person.strip() + ': #' + rank.strip()

    return "Please search for a player"

@hook.command()
def liverank(text):
    return get_rank(text)

@hook.command()
def rank(text):
    return get_rank(text, rtype='not-live')

@hook.command('shittychigh', 'shittycareerhigh')
def careerhigh(text):
    return get_rank(text, rtype='live', mode='career-high')
