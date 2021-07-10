from re import S
from lib import count_dislikes, is_edge_valid
import typing
from structures import Vec, Figure, VerticesList, Input
import copy
from shapely.geometry import Point
import net
import argparse
import time
import itertools
import math

# this file contains a branch-and-bound algorithm to solve the problem by trying all combinations (but in a smart way).The run time can become really terrible, so it won't finish on many problem instances in a reasonable time
# it's reasonable if there are few legal points and if the figure has only few vertices, all of which are highly connected

# returns a set containing all legal points, i.e.Vec within the polygon
def all_legal_points(problem: Input):
    x_coords = [v.x for v in problem.hole]
    y_coords = [v.y for v in problem.hole]
    result = set()
    for x in range(min(x_coords), max(x_coords)+1):
        for y in range(min(y_coords), max(y_coords)+1):
            p = Point((x, y))
            if p.intersection(problem.hole_polygon):
                result.add(Vec(x,y))
    return result

# assumes the point p is within the polygon
def is_point_valid(p: Vec, a: int, fixed: typing.Set[int], problem: Input, solution: VerticesList):
    solution[a] = p
    for b in problem.figure.neighbors[a]:
        if b not in fixed: continue
        if not is_edge_valid(a, b, problem, solution): return False
    return True

def branch_and_bound(fixed: typing.Set[int], remaining: typing.List[Vec], problem: Input, solution: VerticesList, all_legal_points: typing.Set[Vec], optimum: int = 0):
    if not remaining:
        dislikes = count_dislikes(problem, solution)
        print(f"found a solution with {dislikes} dislikes")
        return solution, dislikes
    a = remaining.pop()
    fixed.add(a)
    options = [p for p in all_legal_points if is_point_valid(p, a, fixed, problem, solution)]
    # if len(options) > 2: print(f"point {a} has {len(options)} options")
    best_solution = None
    dislikes = 99999999
    for round, p in enumerate(options):
        if (len(fixed) == 1): print(f"start round {round} of {len(options)}")
        solution[a] = p
        s, d = branch_and_bound(fixed, remaining, problem, solution, all_legal_points)
        if s and d < dislikes:
            best_solution = copy.deepcopy(s)
            dislikes = d
        if d == optimum: break
    remaining.append(a)
    fixed.remove(a)
    return best_solution, dislikes 

# ideas for improvement:
# - compute good order
# - treat order as a tree: if independent component can't find solution, there is no point in continuing
# - store intermediate best solutions, so we can stop early
def heuristic_order(fixed, remaining, problem: Input):
    remaining = set(remaining)
    rev_order = []
    connectivity = dict([(i, 0) for i in remaining])
    for a in remaining:
        for b in problem.figure.neighbors[a]:
            if b in fixed:
                connectivity[a] += 1
    while remaining:
        a = max(connectivity, key=connectivity.get)
        rev_order.append(a)
        remaining.remove(a)
        del connectivity[a]
        for b in problem.figure.neighbors[a]:
            if b in remaining:
                connectivity[b] += 1
    return list(reversed(rev_order))

def run_branch_and_bound_for_perfect_solution(problem: Input):
    legal_points = all_legal_points(problem)
    solution = copy.deepcopy(problem.figure.vertices)
    hole = problem.hole
    figure_indices = range(len(problem.figure.vertices))
    n = len(figure_indices)
    k = len(hole)
    print(f"there are {k} hole vertices and {n} figure vertices, {math.factorial(n) / math.factorial(n-k)} rounds")
    round = 0
    for perm in itertools.permutations(figure_indices, len(hole)):
        round += 1
        fixed = set()
        valid = True
        for i in range(len(hole)):
            fixed.add(i)
            solution[perm[i]] = hole[i]
            if not is_point_valid(hole[i], perm[i], fixed, problem, solution):
                valid = False
                break
        if not valid: continue
        remaining = [i for i in figure_indices if i not in fixed]
        remaining = heuristic_order(fixed, remaining, problem)
        print(f"starting round {round}")
        result, dislikes = branch_and_bound(fixed, remaining, problem, solution, legal_points, 0)
        if result: return result, dislikes
    print("Could not find any perfect solution!")
    return None, -1

def run_branch_and_bound(problem: Input, optimum: int = 0):
    legal_points = all_legal_points(problem)
    solution = copy.deepcopy(problem.figure.vertices)
    remaining = heuristic_order(set(), [i for i in range(len(solution))], problem)
    solution, dislikes = branch_and_bound(set(), remaining, problem, solution,  legal_points, optimum)
    return solution

argparser = argparse.ArgumentParser()
argparser.add_argument('problem', type=int, help="Problem id")
argparser.add_argument('optimum', type=int, help="minimum number of dislikes (algorithm can terminate once it finds a solution of this quality)")
args = argparser.parse_args()
problem = net.load(args.problem)
optimum = args.optimum
start = time.time()
if optimum > 0:
    solution = run_branch_and_bound(problem, optimum)
else:
    run_branch_and_bound_for_perfect_solution(problem)
end = time.time()
print(f"the algorithm took {end - start} seconds")
net.check_and_submit(problem, solution)