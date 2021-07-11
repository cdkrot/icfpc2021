import argparse
from fractions import Fraction
import json

from shapely.geometry import polygon
from shapely.geometry.linestring import LineString
from shapely.geometry.point import Point
from physics import Physics
from lib import count_dislikes
from structures import Figure, Input, Vec, VerticesList
import random
import net

# Physics steps after each mutation
PHYSICS_STEPS = 50

def eval_solution(problem: Input, solution: VerticesList):
    # TODO: Come up with better constants for the penalties
    #       (currently just tweaked per problem)
    polygon = problem.hole_polygon
    penalty = 0.0

    for a,b in problem.figure.edges:
        line = LineString([solution[a].to_tuple(), solution[b].to_tuple()])
        outside = line.difference(polygon).length
        if outside > 0:
            penalty += 1000 + 100 * outside * outside

        dist_orig = (problem.figure.vertices[a] - problem.figure.vertices[b]).len2()
        dist_new = (solution[a] - solution[b]).len2()
        ratio = abs(Fraction(dist_new, dist_orig) - 1)
        bound = Fraction(problem.epsilon, int(1e6))
        if ratio > bound:
            penalty += 1000 + 1000 * float(ratio - bound)

    for v in solution.vertices:
        outside = polygon.distance(Point(v.x, v.y))
        if outside > 0:
            penalty += 1000 + 100 * outside
    
    penalty += count_dislikes(problem, solution)
    
    return penalty

def mutate_solution(problem: Input, solution: VerticesList, deviation: float) -> VerticesList:
    # TODO: Idea, try making it more likely to select vertices that "matter"
    #       e.g. ones that incur a penalty or closest to a hole vertex
    new_vertices = []
    for i, v in enumerate(solution.vertices):
        dx = random.normalvariate(0, deviation)
        dy = random.normalvariate(0, deviation)
        new_vertices.append(v + Vec(dx, dy))

    physics = Physics()
    vs = VerticesList(new_vertices)
    for _ in range(PHYSICS_STEPS):
        vs = physics.apply(problem, VerticesList(vs))

    rounded = VerticesList([Vec(round(p.x), round(p.y)) for p in vs])
    return rounded

def crossover(s1: VerticesList, s2: VerticesList):
    vs = [random.choice([a, b]) for a, b in zip(s1.vertices, s2.vertices)]
    return VerticesList(vs)

def hill_climb(problem: Input, sol: VerticesList):
    num_steps = 100
    num_mutations = 20
    start_deviation = 5
    end_deviation = 1
    for step in range(num_steps):
        deviation  = start_deviation + (end_deviation - start_deviation) * step / (num_steps-1)
        new_sols = [sol] + [mutate_solution(problem, sol, deviation) for _ in range(num_mutations)]
        sol = min(new_sols, key=lambda sol: eval_solution(problem, sol))
        print(step+1, eval_solution(problem, sol))
    return sol

def genetic_alg(problem: Input, init_sol: VerticesList):
    pop_size = 20
    keep_top = 3
    start_deviation = 10
    end_deviation = 1
    num_steps = 100
    crossover_num = 5

    population = [init_sol] * pop_size

    for step in range(num_steps):
        deviation  = start_deviation + (end_deviation - start_deviation) * step / (num_steps-1)

        # keep the top `keep_top`, add mutations for each population member
        # and then all pairwise cross-overs for top `crossover_num`
        new_pop = population[:keep_top]
        for sol in population:
            new_pop.append(mutate_solution(problem, sol, deviation))
        for i in range(crossover_num):
            for j in range(i+1, crossover_num):
                new_pop.append(crossover(population[i], population[j]))
        new_pop.sort(key=lambda sol: eval_solution(problem, sol))

        population = new_pop[:pop_size]
        print(step+1, eval_solution(problem, population[0]))
    
    return population[0]

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('problem', type=int, help="Problem id")
    argparser.add_argument('--vertices', dest="vertices", help="Load vertices from a file (JSON)")
    argparser.add_argument('--output', dest="output", help="File to write vertices to (default stdout)")
    args = argparser.parse_args()
    problem = net.load(args.problem)

    if args.vertices:
        with open(args.vertices) as f:
            vs = VerticesList()
            vs.read_json(json.loads(f.read()))
            print("Loaded vertices:", vs)
    else:
        vs = problem.figure.vertices

    print("Starting..")
    # result = hill_climb(problem, vs)
    result = genetic_alg(problem, vs)
    result_json = json.dumps(result.to_json())
    
    print("Done.\n")
    if args.output:
        with open(args.output, "w") as f:
            f.write(result_json)
            print("Wrote result to file", args.output)
    else:
        print(result_json)

if __name__ == "__main__":
    main()