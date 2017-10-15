import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import json
import matplotlib.pyplot as plt
import pickle

with open('./config.json', 'r') as f:
	data = json.load(f)
	base_url = data['base_url']
	steam_api_key = data['steam_api_key']
	

path_file = './data/steam_user_id.txt'
user_game_inventories = {}
with open(path_file, 'r') as f:
    user_ids = [i for i in f.readlines() if len(i)>2]
    for steam_user_id in user_ids:
        params = {'key' : steam_api_key, 'steamid': steam_user_id  ,'format': 'json'}
        r = requests.get(base_url, params)
        if r.status_code == 200:
            user_game_inventories[steam_user_id] = r.json()['response']
        else:
            print('steam_user_id is ',steam_user_id)
            print('status: fail')
            break
        time.sleep(5)      
print("user_game_inventories are", user_game_inventories)

def save_obj(obj, name ):
    with open('./data/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('./data/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

save_obj(user_game_inventories, "user_game_inventories")
name = "user_game_inventories"
load_user_inventories = load_obj(name)

import datetime
today = datetime.datetime.now()
print(str(today))

path_file = './data/'+str(today)+'_user_inventory.txt'
print(path_file)

with open(path_file, 'w') as f:
    for user_id, json_data in user_game_inventories.items():
        f.write(json.dumps({str(user_id[0:17])[2:-1]: json_data.get('games')}))
        f.write('\n')

print("The number of users' inventories is", len(user_game_inventories))



