import re

# Define input and output file paths
input_file_path = '/Users/mayiran/PycharmProjects/linguistics/en_final.txt'
output_file_path = '/en_final.txt'

# Read file content
with open(input_file_path, 'r') as file:
    content = file.read()

# Split content into lines
lines = content.splitlines()

# Initialize a list to store the processed lines
processed_lines = []

# Define regex patterns
svo_pattern = re.compile(r'(<S>|<V>|<O>)')
adverbial_tags = ['<time>', '<place>', '<manner>', '<cause>', '<effect>', '<purpose>', '<condition>', '<concession>']

# Process each line
for line in lines:
    # Split at the second occurrence of <S>
    parts = re.split(r'(<S>)', line)
    new_line = []
    s_count = 0
    for part in parts:
        if part == '<S>':
            s_count += 1
            if s_count == 2:
                processed_lines.append(''.join(new_line).strip())
                new_line = []
        new_line.append(part)
    if new_line:
        processed_lines.append(''.join(new_line).strip())

# Filter out lines that only contain SVO, only adverbial tags, "NONE", or do not contain <V>
final_lines = []
for line in processed_lines:
    if line.strip() == "NONE" or '<V>' not in line:
        continue
    svo_count = sum(tag in line for tag in ['<S>', '<V>', '<O>'])
    adverbial_count = sum(tag in line for tag in adverbial_tags)
    if (svo_count > 0 and adverbial_count > 0) or (svo_count == 0 and adverbial_count == 0):
        final_lines.append(line)

# Write the processed lines to the new file
with open(output_file_path, 'w') as file:
    for line in final_lines:
        if line:  # Ensure no empty lines are written
            file.write(line + '\n')