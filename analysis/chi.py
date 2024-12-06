import re
import numpy as np
from scipy.stats import chi2_contingency

# 定义从文本中提取数据的正则表达式
pattern = re.compile(r'<(\w+)> List: \[(.*?)\]\nSample Size for <\1>: (\d+)')

input = '/Users/mayiran/PycharmProjects/linguistics/analysis/Q1/ch.txt'

# 读取文件内容
with open(input, 'r') as file:
    content = file.read()

# 提取数据
data = pattern.findall(content)

# 存储结果
results = {}

# 处理每一个状语的数据
for adverbial, values, sample_size in data:
    values = list(map(float, values.split(', ')))
    sample_size = int(sample_size)

    # 创建一个2x2的列联表
    observed = np.array([
        [sum(values), abs(sample_size - sum(values))],
        [abs(len(values) - sum(values)), sum(values)]
    ])

    # 检查 observed 数组是否有负值
    if np.any(observed < 0):
        print(f'Error: Negative value in observed array for {adverbial}')
        print(f'observed: \n {observed}')
        continue

    # 进行卡方检验
    chi2, p, dof, expected = chi2_contingency(observed)

    # 存储结果
    results[adverbial] = chi2, p

# 打印结果
for adverbial, result in results.items():
    print(f'{adverbial}: chi2, p: {result}')