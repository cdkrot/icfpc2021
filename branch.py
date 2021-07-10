from lib import count_dislikes, inside_polygon, is_edge_valid
import typing
from structures import Vec, Figure, VerticesList, Input
import copy
from shapely.geometry import Point
import net
import time

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
# - look for other constraints

def run_branch_and_bound(problem: Input, optimum: int = 0):
    legal_points = all_legal_points(problem)
    print(f"there are {len(legal_points)} legal points")
    solution = copy.deepcopy(problem.figure.vertices)
    solution, dislikes = branch_and_bound(set(), [i for i in range(len(solution))], problem, solution,  legal_points, optimum)
    # finding a suitable order for the number of points significantly accelerates the search
    # solution, dislikes = branch_and_bound(set(), [2, 0, 4, 3, 1], problem, solution,  legal_points)
    print(f"The solution has {dislikes} dislikes")
    print(solution)
    return solution

problem = net.load(36)
optimum = 1444
start = time.time()
solution = run_branch_and_bound(problem, optimum)
end = time.time()
print(f"the algorithm took {end - start} seconds")
net.check_and_submit(problem, solution)