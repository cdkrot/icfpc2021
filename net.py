import requests
from structures import *
import copy
import json

API_TOKEN = '99c449db-fde6-45b8-a07d-2845c5a077d7'


def api_get(url: str, headers=dict()):
    headers = copy.deepcopy(headers)
    headers['Authorization'] = f'Bearer {API_TOKEN}'
    
    r = requests.get(f'https://poses.live/api/{url}', headers=headers)
    return r.json()


def api_post(url: str, data, headers=dict()):
    headers = copy.deepcopy(headers)
    headers['Authorization'] = f'Bearer {API_TOKEN}'
    
    r = requests.post(f'https://poses.live/api/{url}', headers=headers, data=data)
    return r.json()
    

def load(problem: str) -> Input:
    inp = Input()
    inp.read_json(api_get(f'problems/{problem}'))
    return inp


