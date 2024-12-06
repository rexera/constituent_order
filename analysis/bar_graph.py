import re
import matplotlib.pyplot as plt

# 定义文件路径
file_path = '/Users/mayiran/PycharmProjects/linguistics/analysis/Q2/SVO/en.txt'

# 定义正则表达式模式
pattern = re.compile(r'<(\w+)> List: \[(.*?)\]\nSample Size for <\w+>: \d+')

# 读取文件内容
with open(file_path, 'r') as file:
    content = file.read()

# 使用正则表达式查找所有匹配项
matches = pattern.findall(content)

# 解析数据并绘制柱状图
for match in matches:
    label = match[0]
    values = list(map(int, match[1].split(', ')))

    # 计算频率
    freq = [values.count(i) for i in range(1, 5)]

    # 绘制柱状图
    plt.figure()
    plt.bar(range(1, 5), freq, tick_label=[1, 2, 3, 4], edgecolor='black')
    plt.title(f'{label}')
    plt.xlabel('Relative Position Type in SVO Structure')
    plt.ylabel('Frequency')

    # 保存柱状图
    plt.savefig(f'{label}_en.png')
    plt.close()

print("Frequency bar charts have been saved.")