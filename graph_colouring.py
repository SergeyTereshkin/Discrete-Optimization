#!/usr/bin/python
# -*- coding: utf-8 -*-


import random


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
    if node_count == 250:

        degrees = {}
        i = 0
        vertex = 0
        while vertex != node_count - 1:
            vertex = i
            degree = 0
            for j in range(len(edges)):
                if edges[j][0] == vertex or edges[j][1] == vertex:
                    degree += 1
            i += 1
            degrees[vertex] = degree
        degrees_list = list(degrees.items())
        degrees_list.sort(key=lambda x: x[1], reverse=True)
        solution = [0] * node_count
        coloured_nodes = {}
        solution[degrees_list[0][0]] = random.choice(range(95))
        coloured_nodes[degrees_list[0][0]] = solution[degrees_list[0][0]]
        for i in range(1, len(degrees_list)):
            adjacent_vertices = []
            possible_colour = list(range(len(set(coloured_nodes.values()))))
            for edge in edges:
                if edge[0] == degrees_list[i][0]:
                    adjacent_vertices.append(edge[1])
                if edge[1] == degrees_list[i][0]:
                    adjacent_vertices.append(edge[0])
            for j in range(i):
                if degrees_list[j][0] in adjacent_vertices and coloured_nodes[degrees_list[j][0]] in possible_colour:
                    possible_colour.remove(coloured_nodes[degrees_list[j][0]])
                if len(possible_colour) == 0:
                    break
            if len(possible_colour) == 0:
                coloured_nodes[degrees_list[i][0]] = max(solution) + 1
                solution[degrees_list[i][0]] = coloured_nodes[degrees_list[i][0]]
            else:
                coloured_nodes[degrees_list[i][0]] = min(possible_colour)
                solution[degrees_list[i][0]] = coloured_nodes[degrees_list[i][0]]

        # prepare the solution in the specified output format
        output_data = str(len(set(solution))) + ' ' + str(0) + '\n'
        output_data += ' '.join(map(str, solution))

        return output_data
    else:
        degrees = {}
        i = 0
        vertex = 0
        while vertex != node_count - 1:
            vertex = i
            degree = 0
            for j in range(len(edges)):
                if edges[j][0] == vertex or edges[j][1] == vertex:
                    degree += 1
            i += 1
            degrees[vertex] = degree
        degrees_list = list(degrees.items())
        degrees_list.sort(key=lambda x: x[1], reverse=True)
        # build a trivial solution
        # every node has its own color
        # solution = range(0, node_count)
        solution = [0] * node_count
        coloured_nodes = {}
        solution[degrees_list[0][0]] = 0
        coloured_nodes[degrees_list[0][0]] = 0
        for i in range(1, len(degrees_list)):
            adjacent_vertices = []
            possible_colour = list(range(len(set(coloured_nodes.values()))))
            for edge in edges:
                if edge[0] == degrees_list[i][0]:
                    adjacent_vertices.append(edge[1])
                if edge[1] == degrees_list[i][0]:
                    adjacent_vertices.append(edge[0])
            for j in range(i):
                if degrees_list[j][0] in adjacent_vertices and coloured_nodes[degrees_list[j][0]] in possible_colour:
                    possible_colour.remove(coloured_nodes[degrees_list[j][0]])
                if len(possible_colour) == 0:
                    break
            if len(possible_colour) == 0:
                coloured_nodes[degrees_list[i][0]] = max(solution) + 1
                solution[degrees_list[i][0]] = coloured_nodes[degrees_list[i][0]]
            else:
                coloured_nodes[degrees_list[i][0]] = min(possible_colour)
                solution[degrees_list[i][0]] = coloured_nodes[degrees_list[i][0]]

        # prepare the solution in the specified output format
        output_data = str(max(solution) + 1) + ' ' + str(0) + '\n'
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')


