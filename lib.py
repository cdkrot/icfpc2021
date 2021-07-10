from structures import *
from shapely.geometry import LineString, Polygon
from fractions import Fraction
import typing


def on_segment(p: Vec, a: Vec, b: Vec):
    return Vec.cross(a - p, a - b) == 0 and Vec.dot(p - a, p - b) <= 0


def dist(p: Vec, a: Vec, b: Vec):
    if Vec.dot(b - a, p - a) < 0:
        return (p - a).len()
    
    if Vec.dot(a - b, p - b) < 0:
        return (p - b).len()

    return abs((a - p).cross(b - p)) / (a - b).len()


def inside_polygon(p: Vec, polygon: typing.List[Vec]):
    for i in range(len(polygon)):
        if on_segment(p, polygon[i], polygon[(i + 1) % len(polygon)]):
            return True

    count = 0
    for i in range(len(polygon)):
        a = polygon[i]
        b = polygon[(i + 1) % len(polygon)]

        if a.y == b.y:
            continue

        if p.y < min(a.y, b.y) or p.y >= max(a.y, b.y):
            continue
        
        if a.y > b.y:
            a, b = b, a

        if Vec.cross(p - a, b - a) < 0:
            count += 1

    return count % 2 == 1

def is_edge_valid(a: int, b: int, problem: Input, solution: VerticesList, print_message=False):
    polygon = problem.hole_polygon
    line = LineString([solution[a].to_tuple(), solution[b].to_tuple()])
    if line.crosses(polygon):
        if print_message: print(f"edge {a}-{b} crosses polygon")
        return False
    dist_orig = (problem.figure.vertices[a] - problem.figure.vertices[b]).len2()
    dist_new = (solution[a] - solution[b]).len2()
    ratio = abs(Fraction(dist_new, dist_orig) - 1)
    if ratio > Fraction(problem.epsilon, int(1e6)):
        if print_message: print(f"edge {a}-{b} has bad length, target: {dist_orig}, reality: {dist_new}")
        return False
    return True

def is_valid(problem: Input, solution: VerticesList, print_message=False):
    for (a, b) in problem.figure.edges:
        if not is_edge_valid(a, b, problem, solution, print_message):
            return False

    for a in range(len(solution)):
        if not inside_polygon(solution[a], problem.hole.vertices):
            if print_message: print(f"vertex {a} not inside the hole")
            return False

# assumes solution is valid
def count_dislikes(problem: Input, solution: VerticesList):
    dislikes = 0
    for h in problem.hole:
        closest = int(1e18)

        for v in solution:
            closest = min(closest, (h - v).len2())
        dislikes += closest
    return dislikes