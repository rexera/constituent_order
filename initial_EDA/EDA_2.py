import re
from collections import defaultdict, Counter

def analyze_svo_adverbial_patterns(input_file):
    adverbial_tags = ['<time>', '<place>', '<manner>', '<cause>', '<effect>', '<condition>', '<purpose>', '<concession>']
    tag_pattern = re.compile(r'<[^>]+>')  # Match any tag
    svo_pattern = re.compile(r'<S>|<V>|<O>')

    adverbial_distances = defaultdict(lambda: defaultdict(list))
    adverbial_positions = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    svo_adverbial_combinations = Counter()
    adverbial_combinations = Counter()
    pattern_line_indices = defaultdict(list)
    adverbial_line_indices = defaultdict(list)

    with open(input_file, 'r', encoding='utf-8') as infile:
        for line_idx, line in enumerate(infile):
            line = line.strip()
            if line == '<NONE>':
                continue

            matches = [match.group(0) for match in tag_pattern.finditer(line)]
            svo_indices = {tag: idx for idx, tag in enumerate(matches) if tag in ['<S>', '<V>', '<O>']}
            total_tags = len(matches)

            # Check for tightly connected multiple adverbials
            for i in range(len(matches)):
                if matches[i] in adverbial_tags:
                    adverbial_combination = matches[i]
                    for j in range(i + 1, len(matches)):
                        if matches[j] in adverbial_tags:
                            adverbial_combination += matches[j]
                            adverbial_combinations[adverbial_combination] += 1
                            adverbial_line_indices[adverbial_combination].append(line_idx + 1)
                        else:
                            break

            for idx, tag in enumerate(matches):
                if tag in adverbial_tags:
                    for svo_tag, svo_idx in svo_indices.items():
                        distance = abs(idx - svo_idx) / total_tags
                        adverbial_distances[tag][svo_tag].append(distance)
                        if idx < svo_idx:
                            adverbial_positions[tag][svo_tag]['before'] += 1
                        else:
                            adverbial_positions[tag][svo_tag]['after'] += 1

            # Count SVO and adverbial combinations
            pattern = ''.join(matches)
            svo_adverbial_combinations[pattern] += 1
            pattern_line_indices[pattern].append(line_idx + 1)  # Store 1-based line index

    # Calculate average distances
    avg_distances = {tag: {svo: sum(distances) / len(distances) for svo, distances in svo_distances.items()} for tag, svo_distances in adverbial_distances.items()}

    # Calculate probabilities and normalize
    probabilities = {}
    for tag, svo_dict in adverbial_positions.items():
        probabilities[tag] = {}
        for svo_tag, pos_dict in svo_dict.items():
            total = pos_dict['before'] + pos_dict['after']
            probabilities[tag][f'before_{svo_tag}'] = pos_dict['before'] / total
            probabilities[tag][f'after_{svo_tag}'] = pos_dict['after'] / total

    # Get top 50 SVO and adverbial combinations
    top_svo_combinations = svo_adverbial_combinations.most_common(50)
    top_adverbial_combinations = adverbial_combinations.most_common(50)

    return avg_distances, probabilities, top_svo_combinations, pattern_line_indices, top_adverbial_combinations, adverbial_line_indices

# Usage example
input_file = '/Users/mayiran/PycharmProjects/linguistics/crude_anno/extracted_patterns_en.txt'
avg_distances, probabilities, top_svo_combinations, pattern_line_indices, top_adverbial_combinations, adverbial_line_indices = analyze_svo_adverbial_patterns(input_file)

#print("Average Distances of Adverbials from S, V, O:")
#for tag, distances in avg_distances.items():
    #print(f"{tag}: {distances}")

print("\nProbabilities of Adverbials Before/After S, V, O:")
for tag, probs in probabilities.items():
    print(f"{tag}: {probs}")

print("\nTop 50 SVO and Adverbial Combinations with Line Numbers:")
for pattern, count in top_svo_combinations:
    print(f"{pattern}: {count}, Lines: {pattern_line_indices[pattern]}")

print("\nTop 50 Multiple Adverbial Combinations with Line Numbers:")
for combination, count in top_adverbial_combinations:
    print(f"{combination}: {count}, Lines: {adverbial_line_indices[combination]}")