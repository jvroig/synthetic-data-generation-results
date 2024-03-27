import json
import os

# Input and output file paths
input_file_path = 'external/ReviewTags_v1_train.jsonl'
output_file_path = 'ReviewTags_v1_train_002.jsonl'

# Prompt template file path
prompt_template = "external/review_tags_template.json"

# Load prompt template from JSON file
with open(prompt_template, 'r') as template:
    template_data = json.load(template)

def create_prompt(product_name, review_text):
    prompt_string = template_data['prompt'].format(product_name=product_name, review_text=review_text)
    return prompt_string

# Check if the input file exists
if not os.path.exists(input_file_path):
    print(f"Error: The input file '{input_file_path}' does not exist.")
else:
    try:
        # Open the input file and output file
        with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
            line_count = 0
            for line in input_file:
                line_count += 1
                try:
                    # Convert the jsonl string to a dictionary
                    original_data = json.loads(line)

                    # Extract the 'prompt' and 'completion' fields
                    # prompt = original_data.get('prompt')

                    #Extract product name and review text from original data
                    product_name = original_data.get('product_name')
                    review_text = original_data.get('review_text')

                    #Create prompt from product name and review text using json template file
                    prompt = create_prompt(product_name, review_text)
                    completion = original_data.get('tags')

                    # Check if the necessary keys exist
                    if prompt is None or completion is None:
                        print(f"Warning: Missing 'prompt' or 'completion' in line {line_count}.")
                        continue

                    # Define the system message, you can customize this message as needed
                    system_message = """###INSTRUCTIONS###
As a product manager responsible for evaluating customer product reviews, your task is to categorize each review based on its content, acknowledging that a review may warrant zero, one, or multiple tags according to company guidelines.

Available tags are the following: design, peformance, quality, value, none and non-review.

"non-review" - reviews indicating the product has not yet been tried or whose content is simply "I bought this" or "bought this at sale" or "bought this for my wife" with no other useful information or customer sentiment expressed.

A review may receive more than one of these tags/categories if its content encompasses multiple aspects of the product experience. Alternatively, if a review lacks substantial content or does not clearly fit into any category, it may receive a "none" tag. For example, a review that simply says "Good!" or "Excellent!" or "Terrible product!" will end up receiving a "none" tag, because it is not clear which categories will apply due to limited context. These are not classified as "non-review" because they still provided feedback (e.g., that they loved or hated or liked it) despite being not specific enough to be able to determine if it is about value, performance, quality or design.
"""

                    # Create the new data structure for OpenAI fine-tuning format
                    openai_data_format = {
                        "messages": [
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": prompt},
                            {"role": "assistant", "content": completion}
                        ]
                    }

                    # Write the new data structure to the output file in jsonl format
                    output_file.write(json.dumps(openai_data_format) + '\n')

                except json.JSONDecodeError:
                    print(f"Error: Incorrect JSON format in line {line_count}.")
                except Exception as e:
                    print(f"Error processing data in line {line_count}: {e}")

            if line_count == 0:
                print(f"Error: The input file '{input_file_path}' is empty.")
    except IOError as e:
        print(f"Error: An IOError occurred while reading '{input_file_path}' or writing '{output_file_path}': {e}")
