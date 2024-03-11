import csv
from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

client = OpenAI()
# openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message.content

# test code to get a response from the openai api
# prompt = f"""Hello AI
#     """
# print('Prompt: %s' %prompt)
# response = get_completion(prompt)
# print(response)

csv_file="external/v4_prompts.csv"
labels = []
ctr = 0
with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        prompt = row['Prompt_Text']
        
        #Prompt Mmdification
        prompt = prompt[0:-7]
        prompt += """Choose from the options above. Do not explain your answer. Do not include any punctation. 

Answer:"""
        print(prompt)

        rating = row['Rating']
        # response = get_completion(prompt)
        response = "Nega"
        labels.append({'ID': ctr+1, 'Rating': rating, 'Label': response}) 
        ctr=ctr+1



def list_of_dicts_to_csv(data, output_csv):
    if not data:
        print("Error: Empty data list.")
        return

    # Extract field names (header) from the first dictionary in the list
    fieldnames = list(data[0].keys())

    # Write the data to the CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

list_of_dicts_to_csv(labels, "external/v4_labels.csv")