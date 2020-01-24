import csv
import random
import numpy as np 

'''
    csvファイルの読み込み
'''
def read_csv(filename):
    with open(filename + '.csv', 'r') as csv_file:
        data = list(csv.reader(csv_file))
    
    return data

'''
    csvファイルへの書き込み
'''
def write_csv(filename, data):
    with open(filename + '.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for row in data:
            writer.writerow(row)


'''
    親の要素の取得
'''
def choose_parent(data, num_parents):
    weight_list = []
    parents = []
    for elements in range(len(data)):
        weight = len(data) - int(data[elements][len(data[elements]) - 1]) + 1
        for w in range(weight):
            weight_list.append(elements)

    for parent in range(num_parents):
        parent_index = random.choice(weight_list)
        parent_vector = []
        for element in range(len(data[parent_index]) - 1):
            parent_vector.append(float(data[parent_index][element]))
        parents.append(parent_vector)

    return parents

'''
    エリート保存分をリストに追加
'''
def elite_preservation(data, elite_preservation_rate, children):
    for row in data:
        if float(row[len(row) - 1]) <= len(data) * elite_preservation_rate:
            vector = []
            for element in range(len(row) - 1):
                vector.append(float(row[element]))
            children.append(vector)

    return children

'''
    REX
    乱数には正規分布を使用
'''
def REX(parent_vector):
    weight = sum(parent_vector) / len(parent_vector)
    child = weight
    for element in parent_vector:
        child += (element - weight) * np.random.normal(0, 1/len(parent_vector))

    return child

'''
    交叉
'''
def crossover(data, num_parents):
    parents = choose_parent(data, num_parents)
    child = []
    for child_index in range(len(parents[0])):
        parent_vector = []
        for parents_index in range(len(parents)):
            parent_vector.append(parents[parents_index][child_index])
        child.append(REX(parent_vector))

    return child

'''
    新しい世代の作成
'''
def make_children(data, num_parents, elite_preservation_rate):
    children = []
    # エリート保存分
    children = elite_preservation(data, elite_preservation_rate, children)

    # 交叉
    for num_crossover in range(int(len(data) * (1 - elite_preservation_rate))):
        child_vector = crossover(data, num_parents)
        children.append(child_vector)

    return children

'''
    Main
'''
# エリート保存率
elite_preservation_rate = 0.05
# 一度の交叉で使う親の数
num_parents = 2
# 読み込むファイル
read_filename = 'mock_random_matrix'
# 書き込むファイル
write_filename = 'children'

# 対象のデータの読み込み
data = read_csv(read_filename)
# 次の世代の作成
children = []
children = make_children(data, num_parents, elite_preservation_rate)

# 新しい世代をcsvに書き込む
write_csv(write_filename, children)
