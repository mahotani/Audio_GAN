import csv
import numpy as np 
import math
import statistics

'''
    csvファイルへの書き込み
'''
def write_csv(data, filename):
    with open(filename + '.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for row in data:
            writer.writerow(row)

'''
    +1か-1をそれぞれ1/2の確率で出力する
'''
def noise():
    return 1 if np.random.rand() >= 0.5 else -1

'''
    ランダムベクトルの生成
    要素は全て[-1, 1]の範囲
'''
def make_random_vector(num_dimensions):
    random_vector = []
    for dimension in range(num_dimensions):
        random_vector.append(np.random.rand() * noise())

    return random_vector

'''
    ランダム行列の生成
    要素は全て[-1, 1]の範囲
'''
def make_random_matrix(num_elements, num_dimensions):
    random_matrix = []
    for element in range(num_elements):
        random_matrix.append(make_random_vector(num_dimensions))
    
    return random_matrix

'''
    ユークリッド距離
'''
def euclid_distance(vector1, vector2):
    distance = 0
    for index in range(len(vector1)):
        distance = (vector1[index] - vector2[index]) * (vector1[index] - vector2[index])
    
    return math.sqrt(distance)

'''
    各ベクトルのユークリッド距離を取って各ベクトルと他のベクトルとの距離の平均を出し
    最小のもののインデックスを返す。
    各ベクトルの平均と全体の平均と分散も出す。
'''
def each_distance(matrix):
    all_vecotors_mean = []
    for vector in matrix:
        distance_mean = 0
        for index in range(len(matrix)):
            distance_mean += euclid_distance(vector, matrix[index])
        distance_mean /= len(matrix)
        all_vecotors_mean.append(distance_mean)
    
    min = all_vecotors_mean[0]
    index = 0
    for current_index in range(1, len(matrix)):
        if min > all_vecotors_mean[current_index]:
            min = all_vecotors_mean[current_index]
            index = current_index

    all_means = statistics.mean(all_vecotors_mean)
    all_variance = statistics.mean(all_vecotors_mean)
    all_vecotors_mean.append(all_means)
    all_vecotors_mean.append(all_variance)

    return index, all_vecotors_mean

'''
    指定したindexの要素を入れ替える
'''
def replace_element(matrix, index):
    matrix[index] = make_random_vector(len(matrix[index]))
    return matrix

'''
    ユークリッド距離の履歴のcsvファイル用のヘッダーを返す
'''
def header(num_elements):
    header = []
    header.append('試行回数')
    for element in range(num_elements):
        header.append('要素%i' % (element))
    
    header.append('全体の平均')
    header.append('全体の分散')
    return header

'''
    それぞれの要素にランダムになるようにリストの末尾に順位をつける
'''
def add_ranking(random_matrix):
    rank = []
    for index in range(len(random_matrix)):
        rank.append(index + 1)
    
    for swap in range(len(random_matrix)):
        element_index1 = np.random.randint(0, len(random_matrix) - 1)
        element_index2 = np.random.randint(0, len(random_matrix) - 1)
        rank[element_index1], rank[element_index2] = rank[element_index2], rank[element_index1]

    for index in range(len(random_matrix)):
        random_matrix[index].append(rank[index])

    return random_matrix

'''
    Main
'''
# 個体数
num_elements = 20
# 次元数
num_dimensions = 10
# ユークリッド距離の小さい要素を入れ替える回数
num_replace = 10000

# 書き込むファイル
filename = 'mock_random_matrix'

# ユークリッド距離の履歴
euclid_history = []
euclid_history.append(header(num_elements))

# [-1, 1]の範囲でランダム行列を作成
random_matrix = make_random_matrix(num_elements, num_dimensions)
for count in range(1, num_replace + 1):
    index, distances = each_distance(random_matrix)
    distances.insert(0, count)
    euclid_history.append(distances)
    replace_element(random_matrix, index)

# それぞれの個体にランダムでランキングを割り振る
add_ranking(random_matrix)

# 結果をcsvに書き込む
write_csv(random_matrix, filename)

# ユークリッド距離の履歴をcsvファイルに書き込む
write_csv(euclid_history, 'euclid_history')
