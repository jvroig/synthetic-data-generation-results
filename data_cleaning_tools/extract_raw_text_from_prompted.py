import jsonlines
import csv
import re

def extract_review_text(prompt):
    # Use regular expression to extract text between triple backticks
    match = re.search(r'```(.*?)```', prompt, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return ''

def process_jsonl_to_csv(input_jsonl, output_csv):
    with open(input_jsonl, 'r', encoding='utf-8') as json_file:
        data = jsonlines.Reader(json_file)
        
        rows = []
        for line in data:
            review_text = extract_review_text(line['prompt'])
            completion = line['completion']
            rows.append({'prompt': review_text, 'completion': completion})
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['prompt', 'completion']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# Replace 'input_jsonl_path' and 'output_csv_path' with actual file paths
input_jsonl_path = 'HumanJudge_test.jsonl'
output_csv_path = 'HumanJudge_test.csv'

process_jsonl_to_csv(input_jsonl_path, output_csv_path)
