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


result = []
for point in points:
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

final_result = min(result, key=lambda x: x[1])


def improve(solution, initial_distance):
    distance = 0
    for i in range(len(solution) - 1):
        distance_calc = coordinate_matrix.calculate_distance(solution[i], solution[i + 1])
        if distance_calc > distance:
            distance = distance_calc
            point = solution[i + 1]

    closest_point, trip_distance = coordinate_matrix.find_closest_point(point, [])
    solution.remove(point)
    index = solution.index(closest_point)
    solution.insert(index + 1, point)

    new_distance = 0
    for i in range(len(solution) - 1):
        sum_distance = coordinate_matrix.calculate_distance(solution[i], solution[i + 1])
        new_distance += sum_distance
    new_distance += coordinate_matrix.calculate_distance(solution[0], solution[-1])

    return solution, new_distance


improved_result, improved_distance = improve(final_result[0], final_result[1])

out_result = [final_result, [improved_result, improved_distance]]
count = 0
while count < 5000:
    improved_result, improved_distance = improve(improved_result, improved_distance)
    out_result.append([improved_result, improved_distance])
    count += 1

final_out = min(out_result, key=lambda x: x[1])
