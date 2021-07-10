import requests
from structures import *
import lib
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
    
    r = requests.post(f'https://poses.live/api/{url}', headers=headers, data=json.dumps(data))
    return r.json()
    

def load(problem: str) -> Input:
    inp = Input()
    inp.read_json(api_get(f'problems/{problem}'))
    inp.problem_id = problem
    return inp


def submit(problem: str, solution: VerticesList):
    return api_post(f'problems/{problem}/solutions', data={'vertices': solution.to_json()})

def check_and_submit(problem: Input, solution: VerticesList):
    if not lib.is_valid(problem, solution, True): raise RuntimeError("Bad submission")
    dislikes = lib.count_dislikes(problem, solution)

    submit(problem.problem_id, solution)
    print(f"Submitted {problem.problem_id}, expected score is {dislikes}")
