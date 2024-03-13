import csv
import jsonlines

def convert_csv_to_jsonl(input_csv, output_jsonl):
    data = []
    with open(input_csv, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            prompt = row['Prompt']
            completion = row['Completion']
            data.append({'prompt': prompt, 'completion': completion})

    with jsonlines.open(output_jsonl, 'w') as writer:
        for item in data:
            writer.write(item)


split = "test"
input_csv_path = 'processed_' + split + '.csv'
output_jsonl_path = 'dataset_' + split + '.jsonl'

convert_csv_to_jsonl(input_csv_path, output_jsonl_path)
