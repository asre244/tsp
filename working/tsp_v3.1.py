import math
import random
import math
import time
import copy


class CoordinateStorage:
    def __init__(self):
        self.coordinates = {}

    def add_point(self, name, x, y):
        self.coordinates[name] = (x, y)

    def calculate_distance(self, name1, name2):
        x1, y1 = self.coordinates[name1]
        x2, y2 = self.coordinates[name2]
        distance = round(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2), 2)
        return distance

    def find_closest_point(self, name, omitted_options):
        min_distance = float('inf')
        closest_point = None
        for other_name in self.coordinates:
            if other_name != name and other_name not in omitted_options:
                distance = self.calculate_distance(name, other_name)
                if distance < min_distance:
                    min_distance = distance
                    closest_point = other_name
        return closest_point, min_distance


coordinate_matrix = CoordinateStorage()

with open(
        r'C:\Users\AjithSreenivasan\OneDrive - Robinson Bowmaker Paul\Coursera\Discrete Optimization\tsp\data\tsp_51_1',
        'r') as input_data_file:
    input_data = input_data_file.read()
data_list = input_data.split()
data_list = list(map(float, data_list))
n = int(data_list[0])
points = [i for i in range(0, n)]
coordinates = data_list[1:]
coordinate_list = [(i, coordinates[i * 2], coordinates[(i * 2) + 1]) for i in range(0, n)]

for coordinate in coordinate_list:
    coordinate_matrix.add_point(coordinate[0], coordinate[1], coordinate[2])

end_result = []
for point in points:
    print(point)
    result = []
    counter = 0
    total_distance = 0
    points_explored = []
    while counter < n:
        counter += 1
        if counter == 1:
            opt = point
        else:
            opt = next_point
        if counter == n:
            trip_distance = coordinate_matrix.calculate_distance(opt, point)
            points_explored.append(opt)
            total_distance += trip_distance
            break
        points_explored.append(opt)
        next_point, trip_distance = coordinate_matrix.find_closest_point(opt, points_explored)
        total_distance += trip_distance
    result.append([points_explored, total_distance])

    final_result = result[0]
    tour = result[0][0]
    tour_edges = [(tour[i - 1], tour[i]) for i in range(n)]

    improved = True
    while improved:
        improved = False
        for l in range(n):
            for m in range(l + 1, n):
                # current edges
                current_tour_1 = (tour[l], tour[l + 1])
                current_tour_2 = (tour[m], tour[(m + 1) % n])
                current_length = (coordinate_matrix.calculate_distance(current_tour_1[0], current_tour_1[1]) +
                                  coordinate_matrix.calculate_distance(current_tour_2[0], current_tour_2[1]))

                # new_edges
                new_tour_1 = (tour[l], tour[m])
                new_tour_2 = (tour[l + 1], tour[(m + 1) % n])
                new_length = (coordinate_matrix.calculate_distance(new_tour_1[0], new_tour_1[1]) +
                              coordinate_matrix.calculate_distance(new_tour_2[0], new_tour_2[1]))

                if new_length < current_length:
                    improved = True
                    tour[l + 1:m + 1] = tour[l + 1:m + 1][::-1]
                    tour_edges = [(tour[i - 1], tour[i]) for i in range(n)]
    final_tour = [tour_edges[i][0] for i in range(n)]
    new_distance = 0
    for i in range(n):
        sum_distance = coordinate_matrix.calculate_distance(final_tour[i], final_tour[(i + 1) % n])
        new_distance += sum_distance
    print(point, new_distance)
    end_result.append([final_tour, new_distance])
    pass

final_out = min(end_result, key=lambda x: x[1])
