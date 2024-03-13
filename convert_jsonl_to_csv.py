import jsonlines
import csv

def convert_jsonl_to_csv(input_jsonl, output_csv):
    rows = []
    with open(input_jsonl, 'r', encoding='utf-8') as json_file:
        data = jsonlines.Reader(json_file)
        for line in data:
            prompt = line.get('prompt', '')
            completion = line.get('completion', '')
            rows.append({'Prompt': prompt, 'Completion': completion})

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Prompt', 'Completion']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# Replace 'input_jsonl_path' and 'output_csv_path' with actual file paths
input_jsonl_path = 'HumanJudge_test.jsonl'
output_csv_path = 'HumanJudge_test.csv'

convert_jsonl_to_csv(input_jsonl_path, output_csv_path)
