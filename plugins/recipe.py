"""
recipe.py

Provides commands for searching recipes. Also has a number of commands for returning random recipes
in multiple formats.

Created By:
    - Luke Rogers <https://github.com/lukeroge>

License:
    GPL v3
"""

import random

import microdata
import requests
import bs4
import json

from cloudbot import hook
from cloudbot.util import web

BASE_URL = "https://yupitsvegan.com"
SEARCH_URL = BASE_URL + "/?s="
RANDOM_URL = SEARCH_URL + "/surprise"

# set this to true to censor this plugin!
CENSOR = False
PHRASES = [
    "EAT SOME FUCKING \x02{}\x02",
    "YOU WON'T NOT MAKE SOME FUCKING \x02{}\x02",
    "HOW ABOUT SOME FUCKING \x02{}?\x02",
    "WHY DON'T YOU EAT SOME FUCKING \x02{}?\x02",
    "MAKE SOME FUCKING \x02{}\x02",
    "INDUCE FOOD COMA WITH SOME FUCKING \x02{}\x02",
    "CLASSILY PARTAKE IN SOME FUCKING \x02{}\x02",
    "COOK UP SOME FUCKING \x02{}\x02",
    "CURE YOUR MOUTH'S POST TRAUMATIC STRESS DISORDER WITH SOME FUCKING \x02{}\x02",
    "PROCURE SOME CHILD LABOR TO COOK UP SOME FUCKING \x02{}\x02",
    "YOUR INDECISION IS FAR LESS APPETIZING THAN SOME FUCKING \x02{}\x02",
    "PROBABLY FUCK UP SOME FUCKING \x02{}\x02",
    "LESSEN YOUR MOTHER'S SHAME WITH SOME FUCKING \x02{}\x02",
    "EAT SHIT, OR IF YOU DON'T LIKE THAT, SOME FUCKING \x02{}\x02"
]

clean_key = lambda i: i.split("#")[1]


class ParseError(Exception):
    pass


def get_data(url):
    """ Uses the metadata module to parse the metadata from the provided URL """
    try:
        request = requests.get(url)
        request.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        raise ParseError(e)

    result = bs4.BeautifulSoup(request.text, 'html.parser')
    recipe_name = result.find('h2', {'class': 'wprm-recipe-name'}).text
    recipe_description = result.find('div', {'class': 'wprm-recipe-summary'}).text
    print(recipe_name)
    print(recipe_description)
    return recipe_name, recipe_description
    raise ParseError("No recipe data found")


@hook.command(autohelp=False)
def recipe(text, chan, message):
    """[term] - gets a recipe for [term], or gets a random recipe if no term is specified"""
    if text:
        # get the recipe URL by searching
        try:
            search_query_url = SEARCH_URL + text.strip()
            request = requests.get(search_query_url)
            request.raise_for_status()
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
            return "Could not get recipe: {}".format(e)

        search = bs4.BeautifulSoup(request.text)

        # find the list of results
        result_list = search.find('header', {'class': 'entry-header'})
        if result_list:
            results = result_list.find_all('h2', {'class': 'entry-title'})
        else:
            return random.choice(PHRASES).format("Recipe not found")

        # pick a random front page result
        result = bs4.BeautifulSoup(str(random.choice(results)), 'html.parser')

        # extract the URL from the result
        url = result.find('h2').find('a')['href']

    else:
        # get a random recipe URL
        try:
            request = requests.get(RANDOM_URL)
            request.raise_for_status()
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
            return "Could not get recipe: {}".format(e)

        url = request.url

    # use get_data() to get the recipe info from the URL
    print(url)
    try:
        recipe_name, recipe_description = get_data(url)
    except (ParseError, AttributeError) as e:
        return (random.choice(PHRASES) + ' - {} - {}').format("Air", 'www.bullshit.com',
                                                              'A crispy roasted piece of bullshit')

    name = recipe_name.strip()
    final_result = (random.choice(PHRASES) + ' - {} - {}').format(recipe_name, web.try_shorten(url), recipe_description)
    message(final_result, chan)

# inspired by http://whatthefuckshouldimakefordinner.com/ <3
@hook.command("dinner", "wtfsimfd", autohelp=False)
def dinner():
    """- TELLS YOU WHAT THE F**K YOU SHOULD MAKE FOR DINNER"""
    try:
        request = requests.get(RANDOM_URL)
        request.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        return "I CANT GET A DAMN RECIPE: {}".format(e).upper()

    url = request.url

    try:
        data = get_data(url)
    except ParseError as e:
        return "I CANT READ THE F**KING RECIPE: {}".format(e).upper()

    name = data.name.strip().upper()
    text = random.choice(PHRASES).format(name)

    if CENSOR:
        text = text.replace("FUCK", "F**K")

    return "{} - {}".format(text, web.try_shorten(url))
