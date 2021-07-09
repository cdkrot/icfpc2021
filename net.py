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


def check_score(problem: Input, solution: VerticesList):
    from fractions import Fraction
    
    for (a, b) in problem.figure.edges:
        dist_orig = (problem.figure.vertices[a] - problem.figure.vertices[b]).len2()
        dist_new = (solution[a] - solution[b]).len2()

        ratio = abs(Fraction(dist_new, dist_orig) - 1)
        if ratio > Fraction(problem.epsilon, int(1e6)):
            return ('fail', f"edge {a}-{b} has bad length")

    for a in range(len(solution)):
        if not lib.inside_polygon(solution[a], problem.hole.vertices):
            return ('fail', f"vertex {a} not inside the hole")

    dislikes = 0
    for h in problem.hole:
        closest = int(1e18)

        for v in solution:
            closest = min(closest, (h - v).len())
        dislikes += closest
    return ('ok', dislikes)


def check_and_submit(problem: Input, solution: VerticesList):
    sc = check_score(problem, solution)
    if sc[0] != 'ok':
        raise RuntimeError(f"Bad submission (reason: {sc[1]})")

    submit(problem.problem_id, solution)
