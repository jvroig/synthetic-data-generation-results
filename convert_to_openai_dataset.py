import json
import os

# Input and output file paths
input_file_path = 'HumanJudge_eval.jsonl'
output_file_path = 'openai_HumanJudge_eval_003.jsonl'

# Check if the input file exists
if not os.path.exists(input_file_path):
    print(f"Error: The input file '{input_file_path}' does not exist.")
else:
    try:
        # Open the input file and output file
        with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
            line_count = 0
            for line in input_file:
                line_count += 1
                try:
                    # Convert the jsonl string to a dictionary
                    original_data = json.loads(line)

                    # Extract the 'prompt' and 'completion' fields
                    prompt = original_data.get('prompt')
                    completion = original_data.get('completion')

                    # Check if the necessary keys exist
                    if prompt is None or completion is None:
                        print(f"Warning: Missing 'prompt' or 'completion' in line {line_count}.")
                        continue

                    # Define the system message, you can customize this message as needed
                    system_message = """ou are a product manager whose task is to evaluate product reviews from customers. Your evaluation will result in classifying individual reviews into four distinct types based on content and sentiment.The sentiment should be labeled as one of the following options: Positive, Slightly Positive, Negative, Slightly Negative.
                    
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

            if line_count == 0:
                print(f"Error: The input file '{input_file_path}' is empty.")
    except IOError as e:
        print(f"Error: An IOError occurred while reading '{input_file_path}' or writing '{output_file_path}': {e}")
