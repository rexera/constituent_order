import re
from collections import defaultdict

def calculate_adverbial_stats(input_file):
    adverbial_tags = ['<time>', '<place>', '<manner>', '<cause>', '<effect>', '<condition>', '<purpose>', '<concession>']
    tag_pattern = re.compile(r'<[^>]+>')  # Match any tag

    tag_counts = defaultdict(int)
    tag_positions = defaultdict(list)
    total_tags = 0
    total_adverbial_tags = 0
    total_lines = 0
    total_tags_per_line = []

    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.strip()
            if line == '<NONE>':
                continue

            total_lines += 1
            matches = list(tag_pattern.finditer(line))
            total_tags += len(matches)
            total_tags_per_line.append(len(matches))
            line_length = len(line)
            for match in matches:
                tag = match.group(0)
                if tag in adverbial_tags:
                    tag_counts[tag] += 1
                    total_adverbial_tags += 1
                    relative_position = (match.start() + 1) / line_length  # 1-based index
                    tag_positions[tag].append(relative_position)

    tag_avg_positions = {tag: sum(positions) / len(positions) for tag, positions in tag_positions.items()}
    tag_frequencies = {tag: count / total_adverbial_tags for tag, count in tag_counts.items()}
    avg_tags_per_line = sum(total_tags_per_line) / total_lines

    return total_tags, tag_counts, tag_frequencies, tag_avg_positions, avg_tags_per_line

# Usage example
input_file = '/Users/mayiran/PycharmProjects/linguistics/crude_anno/extracted_patterns_en.txt'
total_tags, tag_counts, tag_frequencies, tag_avg_positions, avg_tags_per_line = calculate_adverbial_stats(input_file)

print(f"Total Tags: {total_tags}")
print(f"Average Tags per Line: {avg_tags_per_line:.2f}")

print("\nAdverbial Tag Frequencies and Relative Frequencies:")
for tag, count in tag_counts.items():
    print(f"{tag}: {count} | {tag_frequencies[tag]:.4f}")

print("\nAdverbial Tag Average Positions:")
for tag, avg_pos in tag_avg_positions.items():
    print(f"{tag}: {avg_pos:.2f}")