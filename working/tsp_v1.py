import numpy as np

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
consolidated_list = [(points[i], coordinate_list[i]) for i in range(0, n)]
