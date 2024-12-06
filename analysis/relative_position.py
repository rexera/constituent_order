import re
from collections import defaultdict

def calculate_adverbial_relative_positions(input_file):
    adverbial_tags = ['<time>', '<place>', '<manner>', '<cause>', '<effect>', '<condition>', '<purpose>', '<concession>']
    tag_pattern = re.compile(r'<[^>]+>')  # Match any tag

    # Initialize lists to store relative positions for each adverbial tag
    relative_positions = {tag: [] for tag in adverbial_tags}

    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.strip()
            if line == '<NONE>':
                continue

            matches = [match.group(0) for match in tag_pattern.finditer(line)]
            total_tags = len(matches)

            for idx, tag in enumerate(matches):
                if tag in adverbial_tags:
                    relative_position = idx / total_tags
                    relative_positions[tag].append(relative_position)

    # Print the lists of relative positions and sample size for each adverbial tag
    for tag, positions in relative_positions.items():
        print(f"{tag} List: {positions}")
        print(f"Sample Size for {tag}: {len(positions)}")

# Usage example
input_file = '/Users/mayiran/PycharmProjects/linguistics/en_final.txt'
calculate_adverbial_relative_positions(input_file)