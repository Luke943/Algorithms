import numpy as np


def random_distances(size: int, seed: int) -> np.ndarray:
    """
    Generates pseudo-random distances for an undirected graph of chosen size.
    """

    # generate paths
    nums = []
    for _ in range(4 * size):
        seed = (445 * seed + 700001) % 2097152
        nums.append(seed)

    for i in range(4 * size):
        nums[i] = nums[i] % size + 1

    distances = np.zeros((size, size), int) + np.inf

    # populate distance matrix (using 0 to n-1 for nodes instead of 1 to n)
    for i in range(size):
        v1, d1, v2, d2 = nums[4 * i : 4 * i + 4]
        if (v1 - 1) != i and distances[(i, v1 - 1)] == np.inf:
            distances[(i, v1 - 1)] = d1
            distances[(v1 - 1, i)] = d1
        if (v2 - 1) != i and distances[(i, v2 - 1)] == np.inf:
            distances[(i, v2 - 1)] = d2
            distances[(v2 - 1, i)] = d2

    return distances


def edges_to_array(edges: dict[int : dict[int:int]], size: int) -> np.ndarray:
    """
    Convert edges dictionary to distance array.
    """
    distances = np.zeros((size, size), dtype=int)

    for node1 in edges:
        for node2 in edges[node1]:
            distances[(node1, node2)] = edges[node1][node2]

    return distances


if __name__ == "__main__":
    edges_small = {
        0: {1: 90, 2: 42, 3: 90, 5: 29},
        1: {0: 90, 3: 98, 2: 70, 4: 65},
        2: {0: 42, 1: 70, 5: 30, 3: 36, 4: 97, 6: 46},
        3: {1: 98, 2: 36, 0: 90, 5: 77},
        4: {1: 65, 2: 97, 6: 68},
        5: {2: 30, 3: 77, 0: 29, 6: 90},
        6: {5: 90, 2: 46, 4: 68},
    }
    print(edges_to_array(edges_small, 7))
    edges_large = {
        0: {11: 50, 1: 68, 3: 24, 7: 49, 8: 35, 12: 67, 16: 35},
        1: {0: 68, 10: 99, 12: 67, 11: 34, 2: 30, 3: 14, 4: 52, 7: 90},
        2: {5: 10, 15: 78, 1: 30, 7: 45, 8: 81, 9: 61, 11: 85, 17: 85, 18: 45},
        3: {0: 24, 7: 16, 1: 14, 15: 52, 13: 62, 14: 16},
        4: {1: 52, 15: 92, 6: 17, 8: 27, 9: 13, 10: 15, 18: 45},
        5: {2: 10, 16: 99, 15: 44, 13: 80},
        6: {4: 17, 11: 40, 13: 36, 7: 18, 12: 47, 14: 29, 16: 15, 18: 13},
        7: {3: 16, 6: 18, 1: 90, 0: 49, 2: 45},
        8: {0: 35, 2: 81, 4: 27, 11: 35, 15: 99, 19: 53},
        9: {18: 47, 4: 13, 2: 61, 12: 76, 13: 52},
        10: {1: 99, 4: 15, 18: 33, 12: 19},
        11: {0: 50, 1: 34, 6: 40, 2: 85, 8: 35, 18: 71},
        12: {1: 67, 10: 19, 0: 67, 6: 47, 9: 76, 15: 49, 17: 27},
        13: {5: 80, 6: 36, 3: 62, 9: 52, 15: 48, 14: 82},
        14: {13: 82, 3: 16, 6: 29, 15: 25, 19: 77},
        15: {2: 78, 3: 52, 4: 92, 5: 44, 13: 48, 12: 49, 14: 25, 8: 99},
        16: {5: 99, 6: 15, 0: 35, 18: 33, 17: 85, 19: 23},
        17: {12: 27, 2: 85, 16: 85},
        18: {9: 47, 10: 33, 11: 71, 16: 33, 2: 45, 4: 45, 6: 13},
        19: {16: 23, 14: 77, 8: 53},
    }
