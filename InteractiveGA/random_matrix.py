import csv
import random

'''
    csvファイルへの書き込み
'''
def write_csv(data, filename):
    with open(filename + '.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for row in data:
            writer.writerow(row)

'''
    ランダム行列の生成
    要素は全て[-1, 1]の範囲
'''
def make_random_matrix(num_elements, num_dimensions):
    random_matrix = []
    for element in range(num_elements):
        random_vector = []
        for dim in range(num_dimensions):
            random_vector.append(random.uniform(-1, 1))
        random_matrix.append(random_vector)
    
    return random_matrix

'''
    それぞれの要素にランダムになるようにリストの末尾に順位をつける
'''
def add_ranking(random_matrix):
    rank = []
    for index in range(len(random_matrix)):
        rank.append(index + 1)
    
    for swap in range(len(random_matrix)):
        element_index1 = random.randint(0, len(random_matrix) - 1)
        element_index2 = random.randint(0, len(random_matrix) - 1)
        rank[element_index1], rank[element_index2] = rank[element_index2], rank[element_index1]

    for index in range(len(random_matrix)):
        random_matrix[index].append(rank[index])

    return random_matrix

'''
    Main
'''
num_elements = 20
num_dimensions = 10
filename = 'mock_random_matrix'

random_matrix = make_random_matrix(num_elements, num_dimensions)
add_ranking(random_matrix)

write_csv(random_matrix, filename)
