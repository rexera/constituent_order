import os
import re
from openai import OpenAI
from tqdm import tqdm  # 用于显示进度条
import json

# 初始化 OpenAI 客户端
client = OpenAI()
MODEL = "gpt-4o-mini"

# 读取文件并以换行符分句
def read_and_split_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().strip()

    # 将换行符当作句子结束符，按行分割
    sentences = content.split('\n')

    # 去掉空行
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

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


# 保存结果到文件
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


# 处理多个txt文件，支持断点续推理
def process_multiple_txt_files(input_folder, output_file, prompt_template, batch_size=10, start_file_index=0):

    all_files = sorted(
        [f for f in os.listdir(input_folder) if f.endswith('.txt')],
        key=lambda x: int(re.findall(r'\d+', x)[0]) if re.search(r'\d+', x) else float('inf')
    )

    # 统计总句子数量
    total_sentences = count_total_sentences(input_folder)

    # 进度条设置
    with tqdm(total=total_sentences, desc="Processing sentences", dynamic_ncols=False) as pbar:
        for file_index, file_name in enumerate(all_files):
            if file_index < start_file_index:
                continue

            file_path = os.path.join(input_folder, file_name)
            sentences = read_and_split_txt(file_path)

            # 分批次处理句子
            for i in range(0, len(sentences), batch_size):
                batch_sentences = sentences[i:i + batch_size]
                annotated_sentences = gpt_call_per_sentence(batch_sentences, prompt_template)
                save_results(annotated_sentences, output_file)

                # 更新进度条
                pbar.update(len(batch_sentences))
                print(
                    f"Processed batch {i // batch_size + 1} from file: {file_name}, sentences: {len(batch_sentences)}")


# 示例 prompt 模板（针对中文）
prompt_template = """
请从以下句子中提取下列功能块并标注：

1. 主语 <S>，谓语 <V>，宾语 <O>
2. 功能块（传递固定类型信息），类型如下：

  - 时间：<time> 例如：会议结束后、日出前
  - 地点：<place> 例如：在公园、在机场
  - 方式：<manner> 例如：非常小心地、匆忙地
  - 原因：<cause> 例如：因为下雨、由于病情
  - 结果：<effect> 例如：效果显著、取得胜利
  - 条件：<condition> 例如：如果下雨、除非你快点
  - 目的：<purpose> 例如：为了考试通过、为了和平
  - 让步：<concession> 例如：尽管困难、虽然天气恶劣
  
首先去掉原始数据中的Parsing标记（空格）
然后标注，directly in the sentence, in **one line**, using these tags. 一次生成在一行中，不要换行。
注意：可能会有无主语或无宾语的情况，这时候只需要标注<V><O>或<S><V>即可。
无法判断出来的成分，请尽量在标签中选择一个来标注，**禁止随意删除原句中的任何一个字。**
不允许随意删除原句中的任何一个字。请保留原句中的语序。**禁止为了方便标注而篡改原句语序**
禁止把所有句子都改成S开头！我不需要你把所有句子都改成S开头！千万不要这么做。


例子1：

输入：

广大 基层 民警 纷纷 表示 ， 要 始终 坚持 把 加强 党 的 政治 建设 摆 在 首位。

输出：

<S>广大基层民警</S><manner>纷纷</manner><V>表示</V>，<manner>要 始终 坚持</manner><V>把</V><O>加强党的政治建设</O><place>摆在首位</place>。

例子2:

<effect>“ 总揽 全局 、 内涵 丰富 、 思想 深邃 ” </effect>， <time>连日来</time> ， <S>习近平 总书记在 中央 政法 工作会议 上 的 重要 讲话</S> <place>在 全国 公安机关 基层 民警 中</place> <V>引发</V> <manner>热烈</manner> <O>反响</O> 。

不允许删除这里的：“ 总揽 全局 、 内涵 丰富 、 思想 深邃 ”，连日来，。必须标注。

无主语句如：

<manner>勇</manner><V>担</V><O>使命</O><manner>砥砺前行</manner><manner>不断</manner><V>谱写</V><O>新时代公安工作新篇章</O>

例子3:

端午 小 长假 ， 山东 枣庄 台儿庄 游人 如 织 ， 徜徉 在 大运河 畔 。

<time>端午小长假</time>，<place>山东枣庄台儿庄</place><S>游人</S><manner>如织</manner><V>徜徉</V><place>在大运河畔</place>。

禁止删去：“端午 小 长假 ， 山东 枣庄 台儿庄 ”！！！！！

"""

# 设置输入、输出文件夹和参数
input_folder = "/Users/mayiran/PycharmProjects/linguistics/corpora/ToRCH2019/ToRCH2019_V1.5/A"
output_file = "/Users/mayiran/PycharmProjects/linguistics/ch_annotated.txt"
batch_size = 10
start_file_index = 0

# 执行标注流程
process_multiple_txt_files(input_folder, output_file, prompt_template, batch_size=batch_size,
                           start_file_index=start_file_index)
