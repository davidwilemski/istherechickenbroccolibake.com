
import requests
import argparse
import json


BASEURL = "http://davidwilemski.com/UMichDining/index.php"
APIURI = "/menu/getAllMenus/today"
APIURL = BASEURL + APIURI


def get_menu():
    r = requests.get(APIURL)
    menu = json.loads(r.content)
    return menu


def search_menu_for(menu, food):
    results = []
    for hall, v in menu.items():
        if 'lunch' in v and food in v['lunch']:
            results.append('{} at {} for lunch!'.format(food, hall))
        if 'dinner' in v and food in v['dinner']:
            results.append('{} at {} for dinner!'.format(food, hall))
    return {'results': results}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Checks for your favorite food in the dining hall')
    parser.add_argument(
        'food',
        help='Food to check for. Try "Chicken Broccoli Bake"'
        'or "Chocolate Chip Cookies"')
    args = parser.parse_args()

    results = search_menu_for(get_menu(), args.food)['results']
    if not results:
        print 'Sorry, no {} today! :('.format(args.food)
        exit()
    for i in results:
        print i
