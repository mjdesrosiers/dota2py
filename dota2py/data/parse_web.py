import json

import requests

URL_HEROES = "https://www.dota2.com/datafeed/herolist?language=english"

URL_ITEMS = "https://www.dota2.com/datafeed/itemlist?language=english"

if __name__ == "__main__":
    """
        Parse heroes list
    """
    resp = requests.get(URL_HEROES)
    heroes_json = json.loads(resp.content)['result']['data']['heroes']
    hero_data = []
    for hero in heroes_json:
        hero_dict = {
            "id": hero['id'],
            "localized_name": hero['name_loc'],
            "name": hero['name'],
        }
        hero_data.append(hero_dict)
    hero_json_data = {
        "result": {
            "heroes": hero_data
        }
    }

    with open("heroes.json", "w+") as herofile:
        json.dump(hero_json_data, herofile, indent=2)
    """
        Parse items list
    """
    resp = requests.get(URL_ITEMS)
    items_json = json.loads(resp.content)['result']['data']['itemabilities']
    item_data = []
    for item in items_json:
        item_dict = {
            "id": item['id'],
            "name": item['name_loc'],
        }
        item_data.append(item_dict)
    item_json_data = {
        "result": {
            "items": item_data
        }
    }
    with open("items.json", "w+") as itemfile:
        json.dump(item_json_data, itemfile, indent=2)
    print(resp)
