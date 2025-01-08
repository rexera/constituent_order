import re

# Define input and output file paths
input_file_path = '/Users/mayiran/PycharmProjects/constituent_order/demo/extracted_patterns_ch.txt'
output_file_path = '/Users/mayiran/PycharmProjects/constituent_order/demo/ch_final.txt'

# Read file content
with open(input_file_path, 'r') as file:
    content = file.read()

# Split content into lines
lines = content.splitlines()

# Initialize a list to store the processed lines
processed_lines = []

# Define regex pattern to match S, V, O tags
pattern = re.compile(r'(<S>|<V>|<O>)')

# Process each line
for line in lines:
    matches = pattern.findall(line)
    if matches:
        svo_count = {'<S>': 0, '<V>': 0, '<O>': 0}
        new_line = []
        for tag in re.split(r'(<S>|<V>|<O>)', line):
            if tag in svo_count:
                svo_count[tag] += 1
            new_line.append(tag)
            if svo_count['<S>'] > 1 or svo_count['<V>'] > 1 or svo_count['<O>'] > 1:
                if tag == '<O>':
                    processed_lines.append(''.join(new_line).strip())
                    new_line = []
                    svo_count = {'<S>': 0, '<V>': 0, '<O>': 0}
        if new_line:
            processed_lines.append(''.join(new_line).strip())

# Filter out lines that only contain SVO and no adverbial tags
adverbial_tags = ['<time>', '<place>', '<manner>', '<cause>', '<effect>', '<purpose>', '<condition>', '<concession>']
final_lines = []
for line in processed_lines:
    adverbial_count = sum(tag in line for tag in adverbial_tags)
    if adverbial_count > 0 and all(tag in line for tag in ['<S>', '<V>', '<O>']):
        final_lines.append(line)

# Write the processed lines to the new file
with open(output_file_path, 'w') as file:
    for line in final_lines:
        if line:  # Ensure no empty lines are written
            file.write(line + '\n')