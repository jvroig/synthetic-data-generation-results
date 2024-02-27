import os
import csv
import re


def extract_info_from_file(file_name):
    # Extract sentiment, persona, variant, sentence count, and run from the file name
    segments = file_name.split('_')
    sentiment = segments[0].replace('-', ' ') #dashes to spaces 
    persona = segments[1].replace("-", ' ') #dashes to spaces
    variant = segments[2].replace("-", ' ') #dashes to spaces
    sentence_count = segments[3].replace('s', '') #remove 's' from the segment
    run = re.search(r'run(\d+)', segments[4]).group(1)  # Extract only the final number from the "run" segment

    return sentiment, persona, variant, sentence_count, run

def extract_info_from_file_content(content):
    # Extract product name and review using regex
    product_name_match = re.search(r'"product[\\_]*name": "(.*?)"', content)
    review_match = re.search(r'"review": "(.*?)"', content)

    if product_name_match and review_match:
        product_name = product_name_match.group(1)
        review = review_match.group(1)
        return product_name, review
    else:
        return None, None
    
def process_directory(directory_path, output_csv):
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'sentiment', 'persona', 'variant', 'sentence_count', 'run', 'product_name', 'review_text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        id_counter = 1
        for filename in os.listdir(directory_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                sentiment, persona, variant, sentence_count, run = extract_info_from_file(filename)
                product_name, review = extract_info_from_file_content(content)
                if product_name and review:
                    writer.writerow({'id': id_counter, 'sentiment': sentiment, 'persona': persona, 'variant': variant,
                                     'sentence_count': sentence_count, 'run': run,
                                     'product_name': product_name, 'review_text': review})
                    id_counter += 1

# Replace 'input_directory_path' and 'output_csv_path' with actual directory paths
input_directory_path = 'expid_2024-02-25/output/Mixtral-8x7b-instruct/'
output_csv_path = 'output.csv'

process_directory(input_directory_path, output_csv_path)
process_directory(input_directory_path, output_csv_path)
