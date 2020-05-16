#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import namedtuple
from gurobipy import *
import math




Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])


def length(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])

    facilities = []
    for i in range(1, facility_count + 1):
        parts = lines[i].split()
        facilities.append(Facility(i - 1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3]))))
    solution = []
    customers = []
    for i in range(facility_count + 1, facility_count + 1 + customer_count):
        parts = lines[i].split()
        customers.append(Customer(i - 1 - facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))

    # build a trivial solution
    # pack the facilities one by one until all the customers are served

    m = Model("fp")
    m.setParam('TimeLimit', 600)
    x_w = {}
    for i in range(facility_count):
        x_w[i] = m.addVar(vtype=GRB.BINARY, name="x_w_%d" % i)
    y_wc = {}
    for i in range(facility_count):
        for j in range(customer_count):
            y_wc[(i, j)] = m.addVar(vtype=GRB.BINARY, name="y_wc_%d_%d" % (i, j))
    m.update()
    for i in range(facility_count):
        for j in range(customer_count):
            m.addConstr((y_wc[(i, j)] <= x_w[i]))
    for j in range(customer_count):
        m.addConstr(sum(y_wc[(i, j)] for i in range(facility_count)) == 1 )
    for i in range(len(facilities)):
        m.addConstr(sum(y_wc[(i, j)] * customers[j].demand for j in range(len(customers))) <= x_w[i]* facilities[i].capacity)
    m.setObjective(sum(x_w[i] * facilities[i].setup_cost for i in range(facility_count)) + sum(
        y_wc[(i, j)] * length(facilities[i].location, customers[j].location) for i in range(facility_count) for j in
        range(customer_count)))
    m.modelSense = GRB.MINIMIZE
    m.optimize()
    obj = m.objVal
    for j in range(customer_count):
        for i in range(facility_count):
            if y_wc[(i, j)].x == 1:
                solution.append(i)
                break
    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

