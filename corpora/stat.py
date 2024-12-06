import os
import re
from collections import Counter

def calculate_text_statistics(directory):
    token_counter = Counter()

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    tokens = re.findall(r'\b\w+\b', text)
                    token_counter.update(tokens)

    token_count = sum(token_counter.values())
    type_count = len(token_counter)
    type_token_ratio = (type_count / token_count) * 100 if token_count > 0 else 0

    return token_count, type_count, type_token_ratio

# Usage example
directory = '/Users/mayiran/PycharmProjects/linguistics/corpora/ToRCH2019/ToRCH2019_V1.5/A'
token_count, type_count, type_token_ratio = calculate_text_statistics(directory)

print(f"Total Tokens (形符): {token_count}")
print(f"Total Types (类符): {type_count}")
print(f"Type-Token Ratio (类符/形符比): {type_token_ratio:.2f}%")