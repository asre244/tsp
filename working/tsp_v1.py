import math


def choosing_next_item(opt, chosen_list, counter, n, points_explored_2):

    i = 0
    if counter == 0:
        options = decision_list[opt]
        updated_options = options
    elif counter == n - 1:
        options = decision_list[opt]
        updated_options = [item for item in options if 0 in item[0]]
    else:
        options = decision_list[opt]
        starting_removed_options = [item for item in options if 0 not in item[0]]
        updated_options = [item for item in starting_removed_options if not any(value in points_explored_2 for value in item[0])]
    chosen = updated_options[i]
    next_point = next(item for item in chosen[0] if item != opt)
    condition = bool(set([item for item in choices if item != opt]) & set(last_choice))
    if condition or counter == n - 1:
        choices.remove(opt)
        return chosen, next_point
    else:
        i += 1
        choosing_next_item(opt, chosen_list, counter, n)



def neighbors(distance_matrix, coordinate_list, points):
    trim = 42  # todo: change this to dynamic
    decision_list = []
    last_choice = []
    for i in points:
        connected_points = [j for j in distance_matrix if i in j[0]]
        connected_points_sorted_trimmed = sorted(connected_points, key=lambda x: x[1])[:trim]
        decision_list.append(connected_points_sorted_trimmed)
        test = [k for k in connected_points_sorted_trimmed if 0 in k[0]]
        if i != 0 and test != []:
            last_choice.append(i)
        pass
    return last_choice, decision_list

with open(
        r'C:\Users\AjithSreenivasan\OneDrive - Robinson Bowmaker Paul\Coursera\Discrete Optimization\tsp\data\tsp_51_1',
        'r') as input_data_file:
    input_data = input_data_file.read()
data_list = input_data.split()
data_list = list(map(float, data_list))
n = int(data_list[0])
points = [i for i in range(0, n)]
coordinates = data_list[1:]
coordinate_list = [(coordinates[i * 2], coordinates[(i * 2) + 1]) for i in range(0, n)]
consolidated_list = [(points[i], coordinate_list[i]) for i in range(0, n)]

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

last_choice, decision_list = neighbors(distance_matrix, coordinate_list, points)

counter = 0
total_distance = 0
choices = points
chosen_list = []
points_explored = []
while counter < n:
    if counter == 0:
        opt = 0
        points_explored_2 = points_explored
    else:
        points_explored_2 = points_explored[:-1]
    chosen, opt = choosing_next_item(opt, chosen_list, counter, n, points_explored_2)
    chosen_list.append(chosen)
    points_explored.append(opt)
    total_distance += chosen[1]
    print(counter, chosen)
    counter += 1

point_pairs = [i[0] for i in chosen_list]
result = [item for item in point_pairs[0]]
for i in range(1, len(point_pairs) - 1):
    # Find the difference between the current tuple and the previous tuple
    exclusive_data = set(point_pairs[i]) - set(point_pairs[i - 1])
    # Add the exclusive data to the result list
    result.extend(exclusive_data)

# Convert result to a list and sort it if needed
result = list(result)
print(result)
