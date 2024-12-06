import os
import re
from openai import OpenAI
from tqdm import tqdm  # 用于显示进度条
import json

# 初始化 OpenAI 客户端
client = OpenAI()
MODEL = "gpt-4o-mini"

# 读取文件并分句，改进的分句策略
def read_and_split_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().strip()

    # 替换缩写中的句号，防止误分句
    # 使用特殊符号来临时替换缩写中的句号
    abbreviation_patterns = {
        r"Mr\.": "Mr<dot>",
        r"Mrs\.": "Mrs<dot>",
        r"Ms\.": "Ms<dot>",
        r"Dr\.": "Dr<dot>",
        r"Prof\.": "Prof<dot>",
        r"Sr\.": "Sr<dot>",
        r"Jr\.": "Jr<dot>",
        r"Inc\.": "Inc<dot>",
        r"Ltd\.": "Ltd<dot>",
        r"Jan\.": "Jan<dot>",
        r"Feb\.": "Feb<dot>",
        r"Mar\.": "Mar<dot>",
        r"Apr\.": "Apr<dot>",
        r"Jun\.": "Jun<dot>",
        r"Jul\.": "Jul<dot>",
        r"Aug\.": "Aug<dot>",
        r"Sep\.": "Sep<dot>",
        r"Oct\.": "Oct<dot>",
        r"Nov\.": "Nov<dot>",
        r"Dec\.": "Dec<dot>"
    }

    # 替换缩写中的句号
    for abbr, replacement in abbreviation_patterns.items():
        content = re.sub(abbr, replacement, content)

    # 正则表达式分句：
    # 句子结束符后面是空格，紧跟大写字母作为新句子的开头
    sentence_enders = re.compile(r'(?<=[.!?])\s+(?=[A-Z])')

    # 使用正则表达式分句
    sentences = sentence_enders.split(content)

    # 去掉句子两端的空白符，并且去掉空句子
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    # 将缩写中的占位符还原为句号
    for abbr, replacement in abbreviation_patterns.items():
        sentences = [sentence.replace(replacement, abbr.replace('\\', '')) for sentence in sentences]

    return sentences


# GPT 调用函数，给每个句子生成标注
def gpt(input_sentence, prompt):
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": input_sentence
            }
        ],
    )
    answer = response.choices[0].message.content
    print(answer)
    return answer


# 遍历每个句子进行标注
def gpt_call_per_sentence(sentences, prompt_template):
    all_responses = []
    for sentence in sentences:
        print(sentence)
        prompt = prompt_template.format(sentence=sentence)
        response = gpt(sentence, prompt)
        all_responses.append(response)
    return all_responses


# 保存结果到文件，支持追加写入
def save_results(results, output_file):
    with open(output_file, 'a', encoding='utf-8') as outfile:
        for result in results:
            outfile.write(result + "\n")


# 获取所有文件中的句子总数
def count_total_sentences(input_folder):
    total_sentences = 0
    all_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
    for file_name in all_files:
        file_path = os.path.join(input_folder, file_name)
        sentences = read_and_split_txt(file_path)
        total_sentences += len(sentences)
    return total_sentences


# 处理多个txt文件，按文件名数字顺序排序，支持断点续推理
def process_multiple_txt_files(input_folder, output_file, prompt_template, batch_size=10, start_file_index=0):
    # 获取文件列表并按文件名中的数字顺序排序
    all_files = sorted(
        [f for f in os.listdir(input_folder) if f.endswith('.txt')],
        key=lambda x: int(re.findall(r'\d+', x)[0]) if re.search(r'\d+', x) else float('inf')
    )

    # 统计总句子数量
    total_sentences = count_total_sentences(input_folder)

    # 进度条设置
    with tqdm(total=total_sentences, desc="Processing sentences", dynamic_ncols=False) as pbar:
        for file_index, file_name in enumerate(all_files):
            # 断点续推理，跳过已处理文件
            if file_index < start_file_index:
                continue

            file_path = os.path.join(input_folder, file_name)
            sentences = read_and_split_txt(file_path)

            # 分批次处理句子
            for i in range(0, len(sentences), batch_size):
                batch_sentences = sentences[i:i + batch_size]
                annotated_sentences = gpt_call_per_sentence(batch_sentences, prompt_template)
                save_results(annotated_sentences, output_file)

                # 更新进度条，按句子数量更新
                pbar.update(len(batch_sentences))
                print(f"Processed batch {i // batch_size + 1} from file: {file_name}, sentences: {len(batch_sentences)}")

# 示例 prompt 模板
prompt_template = """
请从以下句子中提取下列功能块并标注：

1. 主语 <S>，谓语 <V>，宾语 <O>
2. 功能块（传递固定类型信息），类型如下：

  - Time: <time>. e.g.: after the meeting, before sunrise, during the summer, in the evening, since last week
  - Place: <place>. e.g.: in the park, at the airport, on the table, by the river, near the school
  - Manner: <manner>. e.g. with great care, in a hurry, by chance, without hesitation, in a friendly manner
  - Cause: <cause>. e.g. because of the rain, due to his illness, owing to a lack of time, on account of the traffic, as a result of the mistake
  - Effect: <effect>. e.g. so well that everyone applauded, too late to catch the bus, fast enough to win the race, so hard that he broke it, so tired that she fell asleep immediately
  - Condition: <condition>. e.g. if it rains, unless you hurry, in case of emergency, provided that you agree, as long as you follow the rules
  - Purpose: <purpose>. e.g. in order to pass the exam, for the sake of peace, so as to finish early, with the aim of improving health, to ensure success
  - Concession: <concession> e.g. despite the difficulties, although it was raining, even though he knew the answer, regardless of the cost, no matter what happens

Please mark:
 1. <S>, <V>, <O> (subject, predicate, object). 
 2. 功能块. 
 directly in the sentence, in **one line**, using these tags.

Only one extraction version is needed. Do not generate multiple annotations.
Original sentence/word needed. Annotate with the original sentence.

directly in the sentence, in **one line**, using these tags. 一次生成在一行中，不要换行。
你需要标注功能块chunk，而非具体的一个两个词。
注意：可能会有无主语或无宾语的情况，这时候只需要标注<V><O>或<S><V>即可。
无法判断出来的成分，请尽量在标签中选择一个来标注，**禁止随意删除原句中的任何一个字。**
不允许随意删除原句中的任何一个字。请保留原句中的语序。**禁止为了方便标注而篡改原句语序**
禁止把所有句子都改成S开头！我不需要你把所有句子都改成S开头！千万不要这么做。

 For example:
 
 Input:
 
Congressional Democrats are united behind sweeping voting rights legislation that won't pass the Senate so long as the filibuster exists, because Republicans are united against it. 
 
 Output:
 
 <S>Congressional Democrats</S><V>are united</V><place>behind sweeping voting rights legislation</place><S><V>won't pass</V><O>the Senate</O><condition>so long as the filibuster exists</condition>,<cause>
 because Republicans are united against it</cause>.
 
例子2：
 
 But on one sliver of voting issues, it seems lawmakers might — might! — be able to agree.
 
 <condition>But on one sliver of voting issues</condition>, <S>it</S> <V>seems lawmakers might — might! — be able</V> <effect>to agree</effect>

 禁止删去But on one sliver of voting issues, it seems ！！！
 
"""

# 使用该函数处理多个txt文件并生成输出文件
input_folder = "/Users/mayiran/PycharmProjects/linguistics/corpora/CROWN2021/CROWN2021_RAW/A"  # 输入txt文件的文件夹路径
output_file = "/Users/mayiran/PycharmProjects/linguistics/en_annotated.txt"  # 生成的标注结果文件
batch_size = 10  # 分批次处理的句子数量
start_file_index = 0  # 设置从哪个文件开始处理，方便断点续推理

# 执行标注流程
process_multiple_txt_files(input_folder, output_file, prompt_template, batch_size=batch_size,
                           start_file_index=start_file_index)
