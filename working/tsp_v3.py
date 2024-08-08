import copy
import math
import random


def choosing_next_item(first_point, first_element, decision_list, choices, last_choice, opt, chosen_list, counter, n,
                       points_explored_2):
    if counter == 0:
        options = decision_list[opt]
        updated_options = options
    elif counter == n - 1:
        options = decision_list[opt]
        updated_options = [item for item in options if first_point in item[0]]
    else:
        options = decision_list[opt]
        starting_removed_options = [item for item in options if first_point not in item[0]]
        updated_options = [item for item in starting_removed_options if
                           not any(value in points_explored_2 for value in item[0])]
    chosen = updated_options[first_element]
    next_point = next(item for item in chosen[0] if item != opt)
    condition = bool(set([item for item in choices if item != opt]) & set(last_choice))
    if condition or counter == n - 1 or counter == n - 2:
        choices.remove(opt)
        return chosen, next_point
    else:
        first_element += 1
        choosing_next_item(first_point, first_element, decision_list, choices, last_choice, opt, chosen_list, counter, n,
                           points_explored_2)


def neighbors(distance_matrix, coordinate_list, points_in_fn):
    # trim = 5000 # todo: change this to dynamic
    decision_list = []
    last_choice = []
    for i in points_in_fn:
        connected_points = [j for j in distance_matrix if i in j[0]]
        connected_points_sorted_trimmed = sorted(connected_points, key=lambda x: x[1])
        decision_list.append(connected_points_sorted_trimmed)
        test = [k for k in connected_points_sorted_trimmed if 0 in k[0]]
        if i != 0 and test != []:
            last_choice.append(i)
        pass
    return last_choice, decision_list


def generating_result_in_format(first_point, chosen_list, total_distance):
    point_pairs = [i[0] for i in chosen_list]
    result = [item for item in point_pairs[0]]
    if result[0] != first_point:
        result.reverse()
    for i in range(1, len(point_pairs) - 1):
        # Find the difference between the current tuple and the previous tuple
        exclusive_data = set(point_pairs[i]) - set(point_pairs[i - 1])
        # Add the exclusive data to the result list
        result.extend(exclusive_data)

    # Convert result to a list and sort it if needed
    result = list(result)
    print(result)

    output_data = str(round(total_distance, 5)) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, result))
    # print(output_data)
    return output_data


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

# revised_data = ''
# for i in points:
#     revised_data += f'{i + 1} {coordinate_list[i][0]} {coordinate_list[i][1]}\n'
#
# with open(r'C:\Users\AjithSreenivasan\OneDrive - Robinson Bowmaker Paul\Coursera\Discrete Optimization\tsp\working\test_data\test.txt', 'w') as file:
#         file.write(revised_data)

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

iterations = 0
while iterations < 500:
    random_list = copy.deepcopy(points)
    random.shuffle(random_list)
    end_result = []
    for first_point in random_list:
        # print(first_point)
        counter = 0
        total_distance = 0
        choices = copy.deepcopy(random_list)
        chosen_list = []
        points_explored = []
        while counter < n:
            if counter == 0:
                opt = first_point
                points_explored_2 = points_explored
            else:
                points_explored_2 = points_explored[:-1]
            chosen, opt = choosing_next_item(first_point, 0, decision_list, choices, last_choice, opt, chosen_list, counter, n,
                                             points_explored_2)
            chosen_list.append(chosen)
            points_explored.append(opt)
            total_distance += chosen[1]
            # print(counter, chosen)
            counter += 1

        # generating_result_in_format(first_point, chosen_list, total_distance)

        # creating a copy
        chosen_list_for_revision = copy.deepcopy(chosen_list)


        def improvement(highest, chosen_list_for_revision, total_distance):
            sorted_chosen_list_for_revision = sorted(chosen_list_for_revision, key=lambda x: x[1], reverse=True)
            # finding the longest edge
            max_dist = sorted_chosen_list_for_revision[highest][1]
            # getting the connecting points of the longest edge
            max_distance_conn = [sorted_chosen_list_for_revision[highest]]
            # getting the edges connecting the two points in the longest edge
            sub_total_list = []
            for j in max_distance_conn[0][0]:
                # print(j)
                chosen_in_solution = [item for item in chosen_list_for_revision if j in item[0]]
                # print(chosen_in_solution)
                sub_total_items = [item[1] for item in chosen_in_solution]
                # finding the sum of the edges from and to the node
                sub_total = sum(sub_total_items)
                sub_total_list.append([j, sub_total])
                pass

            # finding the point with the two longest edges to/from the point
            sorted_sub_total_list = sorted(sub_total_list, key=lambda x: x[1], reverse=True)
            # getting the point to be revised
            causing_point = sorted_sub_total_list[0][0]
            # getting the end point of second edge from the causing point that is to be replaced later
            end_edge_for_revision = [item for item in chosen_list_for_revision if causing_point in item[0]]
            # getting that end point to be replaced
            end_point_for_revision = next(item for item in end_edge_for_revision[1][0] if item != causing_point)
            # getting the shortest edge from the causing point
            option = decision_list[causing_point][0]
            # getting that point
            revision_point = next(item for item in option[0] if item != causing_point)
            # getting the edges around that revision point that will be replaced by the causing edge
            revision_point_in_chosen_list = [item for item in chosen_list_for_revision if revision_point in item[0]]
            starting_edge_for_revision = revision_point_in_chosen_list[1]

            # replacing the points using the causing point
            revised_lines_1 = [(revision_point, causing_point),
                               (causing_point, next(item for item in starting_edge_for_revision[0] if item != revision_point))]
            revised_result_1 = []
            for b in revised_lines_1:
                for a in decision_list[causing_point]:
                    if a[0] == b:
                        revised_result_1.append([b, a[1]])
                    elif a[0][::-1] == b:
                        revised_result_1.append([b, a[1]])
                        break

            # replacing the edge connecting the causing edge and the end_point_for_revision with the end_point_for_revision
            # and the other side of the longest edge
            revised_lines_2 = [(sorted_sub_total_list[1][0], end_point_for_revision)]
            revised_result_2 = []
            for b in revised_lines_2:
                for a in decision_list[end_point_for_revision]:
                    if a[0] == b:
                        revised_result_2.append([b, a[1]])
                    elif a[0][::-1] == b:
                        revised_result_1.append([b, a[1]])
                        break

            # revise end_edge_for_revision with revised_result_2 and starting_edge_for_revision with revised_result_1
            def reordering(A, B, C):
                # Create a new list to store the result
                result = []

                # Replace elements in A with those in C if they match elements in B
                for item in A:
                    if item in B:
                        result.extend(C)
                    elif item[0] == B[0]:
                        result.extend(C)
                    else:
                        result.append(item)
                final_result = []
                [final_result.append(x) for x in result if x not in final_result]
                return final_result

            revised_list = reordering(chosen_list_for_revision, end_edge_for_revision, revised_result_2)
            revised_list = reordering(revised_list, starting_edge_for_revision, revised_result_1)

            revised_distance = sum([item[1] for item in revised_list])

            if len(revised_list) == n:
                return revised_list, revised_distance
            else:
                revised_list, revised_distance = improvement(random.choice(range(1, n)), chosen_list_for_revision, total_distance)
                return revised_list, revised_distance


        solutions = [[chosen_list, total_distance]]
        revised_list, revised_distance = improvement(0, chosen_list_for_revision, total_distance)
        generating_result_in_format(first_point, revised_list, revised_distance)

        while_counter = 0
        while while_counter < 30:
            # try:
            solutions.append([revised_list, revised_distance])
            revised_list, revised_distance = improvement(0, revised_list, revised_distance)
            generating_result_in_format(first_point, revised_list, revised_distance)
            # except:
            #     # solutions.append([revised_list, revised_distance])
            #     revised_list, revised_distance = improvement(1, revised_list, revised_distance)
            #     generating_result_in_format(first_point, revised_list, revised_distance)
            while_counter += 1

        # Find the list with the lowest value and exactly 51 coordinate pairs
        filtered = [item for item in solutions if len(item[0]) == n]
        if filtered:
            min_list = min(filtered, key=lambda x: x[1])
            # print(min_list[1])
        final_result = generating_result_in_format(first_point, min_list[0], min_list[1])
        end_result.append(min_list)

    if end_result:
        min_list = min(end_result, key=lambda x: x[1])
        print(min_list)
    else:
        print("No list with exactly 51 coordinates found.")

    final_result = generating_result_in_format(first_point, min_list[0], min_list[1])
