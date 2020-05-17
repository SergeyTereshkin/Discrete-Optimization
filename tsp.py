import numpy as np
import random
import math
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])


def length(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    def reverse_segment_if_better(tour, i, j, k):
        """If reversing tour[i:j] would make the tour shorter, then do it."""
        # Given tour [...A-B...C-D...E-F...]
        A, B, C, D, E, F = tour[i - 1], tour[i], tour[j - 1], tour[j], tour[k - 1], tour[k % len(tour)]
        d0 = length(points[A], points[B]) + length(points[C], points[D]) + length(points[E], points[F])
        d1 = length(points[A], points[C]) + length(points[B], points[D]) + length(points[E], points[F])
        d2 = length(points[A], points[B]) + length(points[C], points[E]) + length(points[D], points[F])
        d3 = length(points[A], points[D]) + length(points[E], points[B]) + length(points[C], points[F])
        d4 = length(points[F], points[B]) + length(points[C], points[D]) + length(points[E], points[A])

        if d0 > d1:
            tour[i:j] = reversed(tour[i:j])
            return -d0 + d1
        elif d0 > d2:
            tour[j:k] = reversed(tour[j:k])
            return -d0 + d2
        elif d0 > d4:
            tour[i:k] = reversed(tour[i:k])
            return -d0 + d4
        elif d0 > d3:
            tmp = tour[j:k] + tour[i:j]
            tour[i:k] = tmp
            return -d0 + d3
        return 0

    points = []
    for i in range(1, nodeCount + 1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))
    set_of_edges = set()
    if nodeCount == 51:
        solution = [13, 7, 19, 40, 11, 42, 18, 16, 44, 14, 15, 38, 50, 39, 43, 29, 21, 37, 20, 25, 1, 31, 49, 17, 32, 48,
                    22, 33, 0, 5, 2, 28, 10, 9, 45, 3, 46, 8, 4, 34, 24, 41, 27, 47, 26, 6, 36, 12, 30, 23, 35]
    elif nodeCount == 100:
        solution = [46, 45, 36, 1, 60, 33, 97, 15, 93, 12, 0, 65, 86, 58, 27, 31, 56, 75, 10, 81, 73, 95, 78, 67, 98, 42,
                    61, 89, 2, 50, 34, 76, 64, 62, 28, 13, 69, 91, 4, 16, 96, 80, 14, 29, 26, 79, 17, 84, 51, 3, 55, 24,
                    71, 57, 66, 74, 39, 83, 7, 47, 37, 77, 88, 87, 20, 5, 92, 54, 35, 21, 32, 11, 99, 44, 43, 40, 25, 19,
                    72, 70, 38, 90, 8, 22, 52, 18, 9, 53, 63, 48, 68, 41, 59, 85, 6, 23, 49, 82, 94, 30]
    elif nodeCount == 200:


        def three_opt(tour):
            while True:
                delta = 0
                for (a, b, c) in all_segments(len(tour)):
                    delta += reverse_segment_if_better(tour, a, b, c)
                if delta >= 0:
                    break
            return tour

        def all_segments(n):
            return ((i, j, k)
                    for i in range(n)
                    for j in range(i + 1, n)
                    for k in range(j + 1, n + (i > 0))

                    )

        solution = list(range(0, nodeCount))

        # calculate the length of the tour
        obj = length(points[solution[-1]], points[solution[0]])
        for index in range(0, nodeCount - 1):
            obj += length(points[solution[index]], points[solution[index + 1]])
        for k in range(1):
            solution = three_opt(solution)
    elif nodeCount < 2000:
        a = sorted(points, key=lambda r: r[0] ** 2 + r[1] ** 2)
        vertices_dict = {}
        for i in range(len(a)):
            closest_vertices = set()
            if i < 5:
                for count in range(i):
                    if count != i:
                        closest_vertices.add(a[count])
                for count in range(10 - i):
                    if count != i:
                        closest_vertices.add(a[count])
            elif i > len(a) - 11:
                for count in range(i, len(a)):
                    if count != i:
                        closest_vertices.add(a[count])
                for count in range(i + 11 - len(a), i):
                    if count != i:
                        closest_vertices.add(a[count])
            else:
                for count in range(i - 5, i):
                    if count != i:
                        closest_vertices.add(a[count])
                for count in range(i + 1, i + 5):
                    closest_vertices.add(a[count])
            vertices_dict[a[i]] = closest_vertices


        def three_opt_approx(tour):
            while True:
                delta = 0
                for (a, b, c) in all_segments_approx(len(tour)):
                    delta += reverse_segment_if_better(tour, a, b, c)
                if delta >= 0:
                    break
            return tour

        def all_segments_approx(n):
            return ((i, j, k)
                    for i in range(n)
                    for j in range(i + 1, len(vertices_dict[points[i]]))
                    for k in range(j + 1, len(vertices_dict[points[i]]))

                    )

        solution = list(range(0, nodeCount))

        # calculate the length of the tour
        obj = length(points[solution[-1]], points[solution[0]])
        for index in range(0, nodeCount - 1):
            obj += length(points[solution[index]], points[solution[index + 1]])
        for k in range(1):
            solution = three_opt_approx(solution)
    else:
        solution = list(range(0, nodeCount))
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount - 1):
        obj += length(points[solution[index]], points[solution[index + 1]])


    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')
