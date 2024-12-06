import re
import numpy as np
import pandas as pd

# 定义状语标签
adverbial_tags = ['<time>', '<place>', '<manner>', '<cause>', '<effect>', '<condition>', '<purpose>', '<concession>']

# 定义正则表达式模式
tag_pattern = re.compile(r'<[^>]+>')

# 初始化转移矩阵
transition_matrix = np.zeros((len(adverbial_tags), len(adverbial_tags)))

# 读取文件内容
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

# 计算转移矩阵
def calculate_transition_matrix(lines):
    for line in lines:
        line = line.strip()
        if line == '<NONE>':
            continue

        matches = [match.group(0) for match in tag_pattern.finditer(line)]
        adverbial_sequence = [tag for tag in matches if tag in adverbial_tags]

        for i in range(len(adverbial_sequence) - 1):
            current_tag = adverbial_sequence[i]
            next_tag = adverbial_sequence[i + 1]
            current_index = adverbial_tags.index(current_tag)
            next_index = adverbial_tags.index(next_tag)
            transition_matrix[current_index][next_index] += 1

    # 计算转移概率
    for i in range(len(adverbial_tags)):
        total_transitions = np.sum(transition_matrix[i])
        if total_transitions > 0:
            transition_matrix[i] = transition_matrix[i] / total_transitions

# 读取文件并计算转移矩阵
file_path = '/Users/mayiran/PycharmProjects/linguistics/extracted_patterns_ch.txt'
lines = read_file(file_path)
calculate_transition_matrix(lines)

# 使用 pandas 打印转移矩阵
df = pd.DataFrame(transition_matrix, index=adverbial_tags, columns=adverbial_tags)
pd.set_option('display.max_rows', 8)
pd.set_option('display.max_columns', 8)
print(df)

# 提取并排序转移概率
transitions = []
for i, row in enumerate(adverbial_tags):
    for j, col in enumerate(adverbial_tags):
        transitions.append((row, col, transition_matrix[i][j]))

# 按概率从大到小排序
transitions.sort(key=lambda x: x[2], reverse=True)

# 打印排序后的转移概率
for row, col, prob in transitions:
    print(f"{row} -> {col}: {prob:.3f}")