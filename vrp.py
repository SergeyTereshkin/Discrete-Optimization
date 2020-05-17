import math
from collections import namedtuple
import numpy as np

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])






def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])

    customers = []
    for i in range(1, customer_count + 1):
        line = lines[i]
        parts = line.split()
        customers.append(Customer(i - 1, int(parts[0]), float(parts[1]), float(parts[2])))

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
    def reverse_segment_if_better(tour, i, j, k):
        """If reversing tour[i:j] would make the tour shorter, then do it."""
        # Given tour [...A-B...C-D...E-F...]
        A, B, C, D, E, F = tour[i - 1], tour[i], tour[j - 1], tour[j], tour[k - 1], tour[k % len(tour)]
        d0 = length(customers[A], customers[B]) + length(customers[C], customers[D]) + length(customers[E], customers[F])
        d1 = length(customers[A], customers[C]) + length(customers[B], customers[D]) + length(customers[E], customers[F])
        d2 = length(customers[A], customers[B]) + length(customers[C], customers[E]) + length(customers[D], customers[F])
        d3 = length(customers[A], customers[D]) + length(customers[E], customers[B]) + length(customers[C], customers[F])
        d4 = length(customers[F], customers[B]) + length(customers[C], customers[D]) + length(customers[E], customers[A])

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

    def length(customer1, customer2):
        return math.sqrt((customer1.x - customer2.x) ** 2 + (customer1.y - customer2.y) ** 2)


    # the depot is always the first customer in the input
    depot = customers[0]
    dist = np.zeros((len(customers), len(customers)))
    for i in range(1, len(customers)):
        for j in range(0, i):
            dist[i][j] = length(customers[i], customers[j])
    savings = {}
    for i in range(1, len(customers)):
        for j in range(i + 1, len(customers)):
            savings[(i, j)] = length(depot, customers[i]) + length(depot, customers[j]) - dist[j][i]
    savings_list = list((i, savings[i]) for i in savings.keys())
    savings_list.sort(key=lambda r: r[1], reverse=True)

    remaining_capacity = []
    tours = []
    used = set()
    number_i = -1
    number_j = -1
    for (i, j) in np.transpose(savings_list)[:][0]:
        if i not in used and j not in used and len(tours) < vehicle_count :
            tours.append([i, j])
            vehicle_capacity1 = vehicle_capacity - customers[i].demand - customers[j].demand
            remaining_capacity.append(vehicle_capacity1)
            used.add(i)
            used.add(j)
        elif i in used and j in used:
            for tour_number in range(len(tours)):
                if i in tours[tour_number]:
                    number_i = tour_number
                if j in tours[tour_number]:
                    number_j = tour_number
            if number_i != number_j and (tours[number_i][0] == i or tours[number_i][len(tours[number_i]) - 1] == i) and (
                    tours[number_j][0] == j or tours[number_j][
                len(tours[number_j]) - 1] == j):
                if remaining_capacity[number_i] >= sum(customers[j].demand for j in tours[number_j]) and remaining_capacity[number_j] < sum(customers[i].demand for i in tours[number_i]):
                    remaining_capacity[number_i] -= sum(customers[j].demand for j in tours[number_j])
                    tours[number_i].extend(tours[number_j])
                    del tours[number_j]
                    del remaining_capacity[number_j]

                elif remaining_capacity[number_i] < sum(customers[j].demand for j in tours[number_j]) and remaining_capacity[number_j] >= sum(customers[i].demand for i in tours[number_i]):
                    remaining_capacity[number_j] -= sum(customers[i].demand for i in tours[number_i])
                    tours[number_j].extend(tours[number_i])
                    del tours[number_i]
                    del remaining_capacity[number_i]
                elif remaining_capacity[number_i] >= sum(customers[j].demand for j in tours[number_j]) and remaining_capacity[number_j] >= sum(customers[i].demand for i in tours[number_i]):
                    if remaining_capacity[number_i] <= remaining_capacity[number_j]:
                        remaining_capacity[number_i] -= sum(customers[j].demand for j in tours[number_j])
                        tours[number_i].extend(tours[number_j])
                        del tours[number_j]
                        del remaining_capacity[number_j]
                    else:
                        remaining_capacity[number_j] -= sum(customers[i].demand for i in tours[number_i])
                        tours[number_j].extend(tours[number_i])
                        del tours[number_i]
                        del remaining_capacity[number_i]
        else:
            if i not in used:
                for tour_number in range(len(tours)):
                    if j in tours[tour_number]:
                        number_j = tour_number
                if (tours[number_j][0] == j or tours[number_j][len(tours[number_j]) - 1] == j) and remaining_capacity[number_j] >= customers[i].demand:
                    tours[number_j].insert(len(tours[number_j]) - 1, i)
                    remaining_capacity[number_j] -= customers[i].demand
                    used.add(i)
            else:
                for tour_number in range(len(tours)):
                    if i in tours[tour_number]:
                        number_i = tour_number
                        break
            if (tours[number_i][0] == i or tours[number_i][len(tours[number_i]) - 1] == i) and remaining_capacity[
                number_i] >= customers[j].demand:
                tours[number_i].insert(len(tours[number_i]) - 1, j)
                remaining_capacity[number_i] -= customers[j].demand
                used.add(j)

    for tour in range(len(tours)):
        if remaining_capacity[tour] == max(remaining_capacity):
            max_capacity_tour = tour
    customer_set = set(customer.index for customer in customers[1:])
    if len(used) != len(customers[1:]):
        left = customer_set - used
        for customer in left:
            tours[max_capacity_tour].append(customers[customer].index)
            remaining_capacity[max_capacity_tour] -= customers[customer].demand
    if remaining_capacity[len(tours) - 1] < 0:
        for i in range(len(tours)):
            for p in tours[len(tours) - 1]:
                if remaining_capacity[i] >= customers[p].demand:
                        tours[len(tours) - 1].remove(p)
                        remaining_capacity[len(tours) - 1] += customers[p].demand
                        tours[i].append(p)
                        remaining_capacity[i] -= customers[p].demand
    for i in range(len(tours)):
        if remaining_capacity[i] < 0:

            vehicle_tours = []

            remaining_customers = set(customers)
            remaining_customers.remove(depot)

            for v in range(0, vehicle_count):
                vehicle_tours.append([])
                remaining_capacity = vehicle_capacity
                while sum([remaining_capacity >= customer.demand for customer in remaining_customers]) > 0:
                    used = set()
                    order = sorted(remaining_customers,
                                   key=lambda customer: -customer.demand * customer_count + customer.index)
                    for customer in order:
                        if remaining_capacity >= customer.demand:
                            remaining_capacity -= customer.demand
                            vehicle_tours[v].append(customer.index)
                            used.add(customer)
                    remaining_customers -= used

            # checks that the number of customers served is correct
            assert sum([len(v) for v in vehicle_tours]) == len(customers) - 1

            for vehicle_tour in vehicle_tours:
                vehicle_tour.insert(0, 0)
                vehicle_tour = three_opt(vehicle_tour)
            # calculate the cost of the solution; for each vehicle the length of the route
            obj = 0
            for i in range(len(vehicle_tours)):
                for j in range(len(vehicle_tours[i])):
                    if vehicle_tours[i][j] == 0:
                        for num in range(j):
                            permut_object = vehicle_tours[i][num]
                            vehicle_tours[i].append(permut_object)
                        for num in range(j):
                            vehicle_tours[i].remove(vehicle_tours[i][0])
            for v in range(0, vehicle_count):
                vehicle_tour = vehicle_tours[v]
                if len(vehicle_tour) > 0:
                    obj += length(depot, customers[vehicle_tour[0]])
                    for i in range(0, len(vehicle_tour) - 1):
                        obj += length(customers[vehicle_tour[i]], customers[vehicle_tour[i + 1]])
                    obj += length(customers[vehicle_tour[-1]], depot)

            # prepare the solution in the specified output format
            outputData = '%.2f' % obj + ' ' + str(0) + '\n'
            for v in range(0, vehicle_count):
                outputData += ' '.join(
                    [str(customers[customer].index) for customer in vehicle_tours[v]]) + ' ' + str(depot.index) + '\n'

            return outputData

    for tour in tours:
        tour.insert(0, 0)
        tour = three_opt(tour)
    obj = 0
    for i in range(len(tours)):
        for j in range(len(tours[i])):
            if tours[i][j] == 0:
                for num in range(j):
                    permut_object = tours[i][num]
                    tours[i].append(permut_object)
                for num in range(j):
                    tours[i].remove(tours[i][0])
    for v in range(0, len(tours)):
        vehicle_tour = tours[v]
        if len(vehicle_tour) > 0:
            obj += length(depot, customers[vehicle_tour[0]])
            for i in range(0, len(vehicle_tour) - 1):
                obj += length(customers[vehicle_tour[i]], customers[vehicle_tour[i + 1]])
            obj += length(customers[vehicle_tour[-1]], depot)
    outputData = '%.2f' % obj + ' ' + str(0) + '\n'
    for v in range(0, len(tours)):
        outputData +=  ' '.join([str(customers[customer].index) for customer in tours[v]]) + ' ' + str(depot.index) + '\n'
    for v in range(len(tours), vehicle_count):
        outputData += str(depot.index) + ' ' + str(
            depot.index) + '\n'
    return outputData

import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:

        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)')

