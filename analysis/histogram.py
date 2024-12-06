import re
import matplotlib.pyplot as plt

# 定义文件路径
file_path = '/Users/mayiran/PycharmProjects/linguistics/analysis/Q1/ch.txt'

# 定义正则表达式模式
pattern = re.compile(r'<(\w+)> List: \[(.*?)\]\nSample Size for <\w+>: \d+')

# 读取文件内容
with open(file_path, 'r') as file:
    content = file.read()

# 使用正则表达式查找所有匹配项
matches = pattern.findall(content)

# 解析数据并绘制直方图
for match in matches:
    label = match[0]
    values = list(map(float, match[1].split(', ')))

    # 绘制直方图
    plt.figure()
    plt.hist(values, bins=20, edgecolor='black')
    plt.title(f'{label}')
    plt.xlabel('Relative Position')
    plt.ylabel('Frequency')

    # 保存直方图
    plt.savefig(f'{label}_ch.png')
    plt.close()

print("Histograms have been saved.")