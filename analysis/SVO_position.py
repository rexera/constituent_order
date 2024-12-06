import re

# Define file path
file_path = '/Users/mayiran/PycharmProjects/linguistics/en_final.txt'

# Define regex pattern to match any tag in SVO structure
pattern = re.compile(r'<\w+>')

# Read file content
with open(file_path, 'r') as file:
    content = file.read()

# Initialize dictionary to store results
adverbial_positions = {
    'time': [],
    'place': [],
    'manner': [],
    'cause': [],
    'effect': [],
    'condition': [],
    'purpose': [],
    'concession': []
}

# Split content into lines
lines = content.splitlines()

# Process each line to create chunks and find adverbial positions
for line in lines:
    matches = pattern.findall(line)
    if matches:
        # Find the indices of all 'S' tags
        s_indices = [i for i, tag in enumerate(matches) if tag == '<S>']

        # Create chunks starting from each 'S'
        chunks = []
        for i in range(len(s_indices)):
            start_index = s_indices[i]
            end_index = s_indices[i + 1] if i + 1 < len(s_indices) else len(matches)
            chunks.append(matches[start_index:end_index])

        for adverbial in adverbial_positions.keys():
            for chunk in chunks:
                # Remove other adverbial tags from the chunk
                filtered_chunk = [tag for tag in chunk if tag in {'<S>', '<V>', '<O>', f'<{adverbial}>'}]

                # Create a dictionary with index as key and tag as value
                match_dict = {i: tag for i, tag in enumerate(filtered_chunk)}
                if f'<{adverbial}>' in match_dict.values():
                    adverbial_indices = [i for i, tag in match_dict.items() if tag == f'<{adverbial}>' ]

                    for adverbial_index in adverbial_indices:
                        # Find the closest S, V, O indices to the adverbial
                        closest_s_index = min((i for i, tag in match_dict.items() if tag == '<S>'), key=lambda x: abs(x - adverbial_index), default=-1)
                        closest_v_index = min((i for i, tag in match_dict.items() if tag == '<V>'), key=lambda x: abs(x - adverbial_index), default=-1)
                        closest_o_index = min((i for i, tag in match_dict.items() if tag == '<O>'), key=lambda x: abs(x - adverbial_index), default=-1)

                        # Ensure the indices are in the correct order
                        if adverbial_index < closest_s_index or adverbial_index == 1:
                            position = 1
                        elif closest_s_index < adverbial_index < closest_v_index:
                            position = 2
                        elif closest_v_index < adverbial_index < closest_o_index:
                            position = 3
                        elif (adverbial_index > closest_o_index and
                              closest_o_index > closest_v_index and
                              closest_v_index > closest_s_index):
                            position = 4
                        else:
                            print(f'Problematic chunk: {chunk}')
                            continue
                        adverbial_positions[adverbial].append(position)

# Print results
for adverbial, positions in adverbial_positions.items():
    print(f'<{adverbial}> List: {positions}')
    print(f'Sample Size for <{adverbial}>: {len(positions)}')