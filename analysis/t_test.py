import re
import numpy as np
from scipy import stats

# Define the regex pattern to extract data from the text files
pattern = re.compile(r'<(\w+)> List: \[(.*?)\]\nSample Size for <\1>: (\d+)')

# Function to read file content
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to extract data using regex
def extract_data(content):
    return pattern.findall(content)

# Read data from ch.txt and en.txt
ch_content = read_file('/Users/mayiran/PycharmProjects/linguistics/analysis/Q1/ch.txt')
en_content = read_file('/Users/mayiran/PycharmProjects/linguistics/analysis/Q1/en.txt')

ch_data = extract_data(ch_content)
en_data = extract_data(en_content)

# Store t-test results
t_test_results = {}

# Process each adverbial type's data
for (ch_adverbial, ch_values, ch_sample_size), (en_adverbial, en_values, en_sample_size) in zip(ch_data, en_data):
    ch_values = list(map(float, ch_values.split(', ')))
    en_values = list(map(float, en_values.split(', ')))

    # Perform independent samples t-test
    t_stat, p_value = stats.ttest_ind(ch_values, en_values, equal_var=False)
    t_test_results[ch_adverbial] = p_value

# Print t-test results
print("T-Test Results:")
for adverbial, p_value in t_test_results.items():
    print(f'{adverbial}: p-value = {p_value}')