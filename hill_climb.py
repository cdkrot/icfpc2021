import argparse
import json
from physics import Physics
from lib import count_dislikes, count_invalid
from structures import Figure, Input, Vec, VerticesList
import random
import net

# Penalties for invalid vertices/edges when scoring
INVALID_VERTEX = 10000.0
INVALID_EDGE = 1000.0

# Standard deviation for moving around vertices
MUTATE_DEV = 20

# Physics steps after each mutation
PHYSICS_STEPS = 100

# Hill climbing params
HILL_CLIMB_STEPS = 100
HILL_CLIMB_POP = 20

def eval_solution(problem: Input, solution: VerticesList) -> float:
    invalid_edges, invalid_vertices = count_invalid(problem, solution)
    dislikes = count_dislikes(problem, solution)
    return INVALID_VERTEX * invalid_vertices + INVALID_EDGE * invalid_edges + dislikes

def mutate_solution(problem: Input, solution: VerticesList) -> VerticesList:
    # Very naive mutation:
    # 1. pick a random vertex
    # 2. move it some random amount
    # 3. apply some physics to correct the structure (with vertex pinned)
    # 4. round vertices to integers
    to_move = random.randrange(len(solution))
    dx = random.normalvariate(0, MUTATE_DEV)
    dy = random.normalvariate(0, MUTATE_DEV)

    new_vertices = []
    pinned = []
    for i, v in enumerate(solution.vertices):
        if i == to_move:
            new_vertices.append(v + Vec(dx, dy))
            pinned.append(True)
        else:
            new_vertices.append(v)
            pinned.append(False)

    physics = Physics(is_pinned=pinned)
    vs = VerticesList(new_vertices)
    for _ in range(PHYSICS_STEPS):
        vs = physics.apply(problem, VerticesList(new_vertices))

    rounded = VerticesList([Vec(round(p.x), round(p.y)) for p in vs])
    return rounded

def hill_climb(problem: Input, sol: VerticesList):
    for step in range(HILL_CLIMB_STEPS):
        new_sols = [sol] + [mutate_solution(problem, sol) for i in range(HILL_CLIMB_POP)]
        sol = min(new_sols, key=lambda sol: eval_solution(problem, sol))
        print(step+1, eval_solution(problem, sol))
    return sol

# TODO: Try beam search
# TODO: Try some genetic algorithm with crossover
# TODO: Better mutation 

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
    result = hill_climb(problem, vs)
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