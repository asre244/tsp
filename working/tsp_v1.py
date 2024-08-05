import math


def neighbors(distance_matrix, coordinate_list, points):
    trim = 3  # todo: change this to dynamic
    # neighbor_list = []
    decision_list = []
    for i in points:
        connected_points = [j for j in distance_matrix if i in j[0]]
        # connected_points = [j for j in distance_matrix if (i in j[0] and j[0] not in neighbor_list)]
        connected_points_sorted_trimmed = sorted(connected_points, key=lambda x: x[1])[:trim]
        # neighbor_list.extend([item[0] for item in connected_points_sorted_trimmed])
        decision_list.append(connected_points_sorted_trimmed)
        pass
    pass

with open(
        r'C:\Users\AjithSreenivasan\OneDrive - Robinson Bowmaker Paul\Coursera\Discrete Optimization\tsp\data\tsp_5_1',
        'r') as input_data_file:
    input_data = input_data_file.read()
data_list = input_data.split()
data_list = list(map(float, data_list))
n = int(data_list[0])
points = [i for i in range(0, n)]
coordinates = data_list[1:]
coordinate_list = [(coordinates[i * 2], coordinates[(i * 2) + 1]) for i in range(0, n)]
# consolidated_list = [(points[i], coordinate_list[i]) for i in range(0, n)]

pairs = []
for i in range(len(coordinate_list)):
    for j in range(i + 1, len(coordinate_list)):
        pairs.append((i, j))

distance_matrix = []
for pair in pairs:
    a = coordinate_list[pair[0]]
    b = coordinate_list[pair[1]]
    distance = round(math.sqrt(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)), 2)
    distance_matrix.append([pair, distance])

neighbors(distance_matrix, coordinate_list, points)
