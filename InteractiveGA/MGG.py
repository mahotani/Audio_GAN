import csv
import numpy as np
import functions

'''
    交叉
'''
def crossover(parents):
    child = []
    for child_index in range(len(parents[0])):
        parents_vector = []
        for parents_index in range(len(parents)):
            parents_vector.append(parents[parents_index][child_index])
        child.append(functions.REX(parents_vector))
    
    return child

'''
    MGGによる次世代の生成
'''
def next_generation_MGG(data, solutions, bias, num_parents, num_children, num_elite_preservation):
    
    parents, parents_index = functions.random_parent(data, num_parents)
    # print(parents_index)
    for index in range(len(parents_index)):
        count = 0
        for index2 in range(index):
            if parents_index[index2] < parents_index[index]:
                count += 1
        del data[parents_index[index] - count]
    
    children = []

    for parent in parents:
        children.append(parent)

    for cross in range(num_children):
        child_vector = crossover(parents)
        children.append(child_vector)

    evaluations = functions.get_evaluations_list(children, solutions, bias)
    rank_list = functions.get_ranking_list(evaluations)
    # print(rank_list)
    # print(evaluations)
    # 上位のものを元のリストに戻す
    for order in range(1, num_elite_preservation + 1):
        for index in range(len(rank_list)):
            if rank_list[index] == order:
                data.append(children[index])
                del children[index]
                del rank_list[index]
                break
    
    # print(functions.get_evaluations_list(children, solutions, bias))
    # ルーレット選択により選ばれた個体を一つ戻す
    selected = functions.choose_roulette(children, (num_parents - num_elite_preservation), solutions, bias)
    for element in selected:
        data.append(element)

    return data


'''
    Main
'''
# エリート保存数
num_elite_preservation = 1
# 一度の交叉で使う親の数
num_parents = 2
# 一度の交叉で生まれる子の数
num_children = 4
# 読み込むファイル
read_filename = 'pre_experiment/mock_random_matrix_200'
# 書き込むファイル
write_filename = 'MGG/children'
# 実行回数
num_execute = 334

# 局所解ファイル
solutions_file = 'pre_experiment/mock_solutions_200'
# 評価結果のファイル
result_file = 'MGG/evaluation_result'


# 局所解ファイルの読み込み
solutions_data = functions.read_csv(solutions_file)
del solutions_data[0]
solutions_data = functions.transform_to_float(solutions_data)

# 局所解とバイアスに分ける
solutions, bias = functions.divide_solutions_bias(solutions_data)

# 評価値の結果のリスト
evaluations_result = []

for num_experiment in range(1, 3501):
    print(num_experiment)
    # 対象のデータの読み込み
    data = functions.read_csv(read_filename)
    del data[0]
    data = functions.transform_to_float(data)
    before_index = functions.get_result(data, functions.get_evaluations_list(data, solutions, bias), num_experiment, functions.get_best_solution_index(bias), solutions)[2]
    # 次の世代の作成
    for num in range(num_execute):
        print('-------')
        
        # print(functions.get_evaluation_value(data[before_index], solutions, bias))
        data = next_generation_MGG(data, solutions, bias, num_parents, num_children, num_elite_preservation)
        
        print(functions.get_result(data, functions.get_evaluations_list(data, solutions, bias), num_experiment, functions.get_best_solution_index(bias), solutions))
        # before_index = functions.get_result(data, functions.get_evaluations_list(data, solutions, bias), num_experiment, functions.get_best_solution_index(bias), solutions)[2]
    # 新しい世代をcsvに書き込む
    # functions.write_csv(write_filename + '_%i' % num_experiment, data)

    evaluations = functions.get_evaluations_list(data, solutions, bias)
    evaluation_vector = functions.get_result(data, evaluations, num_experiment, functions.get_best_solution_index(bias), solutions)
    evaluations_result.append(evaluation_vector)
final_result = functions.get_final_result(evaluations_result)

functions.write_result(result_file, evaluations_result, final_result)