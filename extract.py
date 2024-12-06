import re

def extract_patterns_per_sentence(input_file, output_file):
    pattern = re.compile(r'<(S|V|O|manner|time|place|cause|effect|condition|purpose|concession)>')
    merge_pattern = re.compile(r'(<(S|V|O|manner|time|place|cause|effect|condition|purpose|concession)>)\1*')
    svo_pattern = re.compile(r'^(<S>|<V>|<O>)+$')
    no_v_pattern = re.compile(r'^(?!.*<V>).*<S>.*$')

    valid_line_count = 0

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            line = line.strip()
            if not line or '<NONE>' in line:
                outfile.write('<NONE>\n')
                continue

            matches = pattern.findall(line)
            if matches:
                extracted_line = ''.join(f'<{match}>' for match in matches)
                merged_line = merge_pattern.sub(r'\1', extracted_line)
                if svo_pattern.match(merged_line) or no_v_pattern.match(merged_line):
                    outfile.write('<NONE>\n')
                else:
                    outfile.write(merged_line + '\n')
                    valid_line_count += 1
            else:
                outfile.write('<NONE>\n')

    print(f'Valid lines: {valid_line_count}')

# Usage example
input_file = 'en_annotated.txt'
output_file = 'extracted_patterns_en.txt'
extract_patterns_per_sentence(input_file, output_file)