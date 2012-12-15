
import requests
import argparse
from xml.etree import ElementTree as ET


BASEURL = 'http://www.housing.umich.edu/files/helper_files/js/menu2xml.php?location={}&date=today'
dining_halls = {
        'barbour': BASEURL.format('BARBOUR%20DINING%20HALL'),
        'bursley': BASEURL.format('BURSLEY%20DINING%20HALL'),
        'couzens': BASEURL.format('COUZENS%20DINING%20HALL'),
        'east-quad': BASEURL.format('BARBOUR%20DINING%20HALL'),
        'lloyd': BASEURL.format('LLOYD%20DINING%20HALL'),
        'markley': BASEURL.format('MARKLEY%20DINING%20HALL'),
        'south-quad': BASEURL.format('SOUTH%20QUAD%20DINING%20HALL'),
        'stockwell': BASEURL.format('STOCKWELL%20DINING%20HALL'),
        'west-quad': BASEURL.format('WEST%20QUAD%20DINING%20HALL'),
        'marketplace': BASEURL.format('MARKETPLACE'),
        'north-quad': BASEURL.format('North%20Quad%20Dining%20Hall'),
        'twigs-at-oxford': BASEURL.format('Twigs%20at%20Oxford'),
}


# Todo: Add support for returning the meal that has the food
# Also: Removing quad for-loop would be fantastic
def search_menu_for(menu, food):
    for meal in menu.find('menu').findall('meal'):
        for station in meal.findall('station'):
            for course in station.findall('course'):
                for menuitem in course.findall('menuitem'):
                    if food.lower() in menuitem.text.strip().lower():
                        return True


def get_menu(url):
    r = requests.get(url)
    tree = ET.fromstring(r.text)
    return tree


def search_all_menus(food):
    results = []
    for key, url in dining_halls.iteritems():
        if search_menu_for(get_menu(url), food):
            results.append(key)
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Checks for your favorite food in the dining hall')
    parser.add_argument(
        'food',
        help='Food to check for. Try "Chicken Broccoli Bake"'
        'or "Chocolate Chip Cookies"')
    args = parser.parse_args()

    results = search_all_menus(args.food)

    if not results:
        print 'Sorry, no {} today! :('.format(args.food)
        exit()

    print args.food, 'is at:'
    for i in results:
        print i
