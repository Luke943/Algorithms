"""
Pathfinding algorithms
"""

import numpy as np
from itertools import combinations


LARGE_DIST = 1 << 28  # Number larger than any path lengths.


def breadth_first_search(
    edges: dict[int : set[int]], source: int, sink: int
) -> list[int]:
    """
    Returns a path from source to sink using a breadth-first search.
    edges is a dictionary of the form {key_node: {all nodes adjacent to key_node}}.
    source and sink are the nodes to find a path from and to.
    """
    seen = [-1] * (max(edges) + 1)
    unvisited = set(edges.keys())
    queue = [[source, -1]]
    path_found = False
    while queue:
        node, fromNode = queue.pop(0)
        if node == sink:
            seen[sink] = fromNode
            path_found = True
            break
        if node in unvisited:
            seen[node] = fromNode
            unvisited.remove(node)
            neighbours = list(edges[node])
            neighbours.sort(reverse=True)
            queue += [[x, node] for x in neighbours]

    if not path_found:
        return []

    path = [sink]
    while path[-1] != source:
        path.append(seen[path[-1]])
    path.reverse()
    return path


def depth_first_search(
    edges: dict[int : set[int]], source: int, sink: int
) -> list[int]:
    """
    Returns a path from source to sink using a depth-first search.
    edges is a dictionary of the form {key_node: {all nodes adjacent to key_node}}.
    source and sink are the nodes to find a path from and to.
    """
    seen = [-1] * (max(edges) + 1)
    unvisited = set(edges.keys())
    stack = [[source, -1]]
    path_found = False
    while stack:
        node, fromNode = stack.pop(-1)
        if node == sink:
            seen[sink] = fromNode
            path_found = True
            break
        if node in unvisited:
            seen[node] = fromNode
            unvisited.remove(node)
            neighbours = list(edges[node])
            neighbours.sort(reverse=True)
            stack += [[x, node] for x in neighbours]

    if not path_found:
        return []

    path = [sink]
    while path[-1] != source:
        path.append(seen[path[-1]])
    path.reverse()
    return path


def dijkstra(distances: np.ndarray, start: int) -> np.ndarray:
    """
    Perform Dijkstra's algorithm and returns shortest path length from start to each node.
    Distance of zero is treated as no path exisiting.
    """
    n = distances.shape[0]
    minDists = np.zeros(n, float) + np.inf
    prevNodes = np.zeros(n, int) - 1

    minDists[start] = 0
    unvisited = {x for x in range(n)}

    while unvisited:
        tmpDict = {i: minDists[i] for i in unvisited}
        x = min(tmpDict, key=tmpDict.get)
        unvisited.remove(x)

        for y, d in enumerate(distances[x]):
            if not distances[(x, y)]:
                continue
            testDist = distances[(x, y)] + minDists[x]
            if testDist < minDists[y]:
                minDists[y] = testDist
                prevNodes[y] = x

    return minDists


def tsp(distances: np.ndarray, start: int, loop=False) -> (int | float, list[int]):
    """
    Run the Travelling Salesman Problem on the distance array with chosen start node.
    Returns pair with (optimal distance, route (as list of nodes)).
    loop determines whether the route loops back to the start node or not.
    Distance of zero is treated as no path exisiting.
    """
    N = len(distances)
    memo = np.zeros((N, 2**N), dtype=distances.dtype)

    setup(distances, memo, start, N)
    solve(distances, memo, start, N)
    minDist = find_min_dist(distances, memo, start, N, loop)
    tour = find_optimal_tour(distances, memo, start, N, minDist, loop)

    return (minDist, tour)


"""
All functions below are helpers for tsp.
"""


def setup(distances, memo, start, N):
    # puts in memo distances of direct path from start to each node
    for i in range(N):
        if i == start:
            continue
        # raise specific bits to concisely denote nodes visited
        dist = distances[start][i]
        memo[i][1 << start | 1 << i] = dist if dist else LARGE_DIST


def solve(distances, memo, start, N):
    # look at all subtours
    for r in range(3, N + 1):
        for subtour in subtours(r, N):
            # generate all possible subtours
            if not_in(start, subtour):
                continue
            for nextNode in range(N):
                if nextNode == start or not_in(nextNode, subtour):
                    # dont consider start or if not in subset
                    continue
                state = subtour ^ (1 << nextNode)  # bitwise xor
                minDist = LARGE_DIST
                for end in range(N):
                    # consider all possible ends
                    if (
                        end == start
                        or end == nextNode
                        or not_in(end, subtour)
                        or distances[end][nextNode] == 0
                    ):
                        # ignore start, next and ones not in subtour
                        continue
                    newDist = memo[end][state] + distances[end][nextNode]
                    if newDist < minDist:
                        minDist = newDist
                # record min distance to cover a subtour
                memo[nextNode][subtour] = minDist


def subtours(r, N):
    # generate all numbers with r bits raised out of first N bits
    combos = combinations(range(N), r)
    subtours = []
    for combo in combos:
        x = 0
        for num in combo:
            x += 1 << num
        subtours.append(x)
    return subtours


def not_in(i, subtour):
    return (1 << i & subtour) == 0


def find_min_dist(distances, memo, start, N, loop):
    # full tour has all bits raised i.e. 2**N - 1
    fullTour = (1 << N) - 1
    nodes = list(range(N))
    nodes.remove(start)
    if loop:
        return min(
            [
                memo[end][fullTour] + distances[end][start]
                for end in nodes
                if distances[end][start]
            ]
        )
    else:
        return min([memo[end][fullTour] for end in nodes])


def find_optimal_tour(distances, memo, start, N, minDist, loop):
    state = (1 << N) - 1
    tour = [start]
    if loop:
        tour = [start, start]
        lastNode = start
    else:
        tour = [start]
        lastNode = -1

    for _ in range(N - 1):
        # populate tour list from end
        for end in range(N):
            if end == start or not_in(end, state):
                continue
            if lastNode == -1:
                # condition to cover first loop where nowhere to go
                distToLast = 0
            else:
                distToLast = distances[end][lastNode]
            newDist = memo[end][state] + distToLast
            if newDist == minDist:
                lastNode = end
                break
        tour.insert(1, lastNode)
        minDist -= distToLast
        state = state ^ (1 << lastNode)

    return tour


if __name__ == "__main__":
    # tests
    connections = {
        0: {1, 2, 3},
        1: {0, 4},
        2: {0, 3, 5},
        3: {0, 2, 4, 6},
        4: {1, 3, 6},
        5: {2, 6},
        6: {3, 4, 5},
    }
    print(breadth_first_search(connections, 0, 6))
    print(depth_first_search(connections, 0, 6))

    distances = np.array(
        (
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 3],
            [1, 0, 1, 1, 0, 0, 0, 9, 0, 9],
            [0, 1, 0, 0, 0, 0, 0, 3, 0, 0],
            [0, 1, 0, 0, 3, 7, 0, 1, 0, 0],
            [0, 0, 0, 3, 0, 5, 0, 0, 0, 0],
            [0, 0, 0, 7, 5, 0, 0, 7, 7, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 9, 3, 1, 0, 7, 1, 0, 0, 7],
            [0, 0, 0, 0, 0, 7, 0, 0, 0, 0],
            [3, 9, 0, 0, 0, 0, 1, 7, 0, 0],
        )
    )
    min_distances = dijkstra(distances, 0)
    print(min_distances)

    distances = np.array(
        (
            [0, 90, 42, 90, 0, 29, 0],
            [90, 0, 70, 98, 65, 0, 0],
            [42, 70, 0, 36, 97, 30, 46],
            [90, 98, 36, 0, 0, 77, 0],
            [0, 65, 97, 0, 0, 0, 68],
            [29, 0, 30, 77, 0, 0, 90],
            [0, 0, 46, 0, 68, 90, 0],
        )
    )
    print(tsp(distances, 0))
    print(tsp(distances, 0, True))
