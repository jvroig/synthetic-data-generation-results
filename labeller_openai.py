import csv
from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

client = OpenAI()
# openai.api_key  = os.getenv('OPENAI_API_KEY')

#gpt-3.5-turbo-0125, gpt-4-0125-preview
def get_completion(prompt, model="gpt-3.5-turbo-0125"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
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
        prompt = """
You are a product manager whose task is to evaluate product reviews from customers. Your evaluation will result in classifying individual reviews into one of four categories according to company guidelines:

1. Positive
The review should reflect a high level of satisfaction with the product. The customer expresses clear satisfaction with multiple aspects of the product. There might be a mention of minor complaints, but the language used indicates a strong likelihood of repurchase or continued use. Words and phrases like "love," "perfect," "exceeds expectations," or "highly recommend" are common. The customer's tone is often enthusiastic or highly approving, or simply lack any criticism.

2. Slightly Positive
The review is generally favorable but may include complaints or suggestions for improvement. The customer seems satisfied with the product but not overly enthusiastic. Positive comments outweigh negative ones, but the reviewer may offer criticism or mention small issues alongside their praise. The overall tone should be more positive than negative. There should be an indication that the customer appreciates the product despite having issues.

3. Slightly Negative
Assign a "Slightly Negative" label in the following cases:
- The review contains criticism of the product but is not wholly negative
- The review only contains mild criticism.  
- The review contains a mix of criticism and mild approval, with a tone leaning more towards disappointment than satisfaction.

4. Negative
The review indicates significant dissatisfaction with the product. The customer may describe multiple aspects of the product as unsatisfactory. The language used is clearly unhappy, disappointed, or frustrated. There is no indication of a willingness to repurchase, and there might be a mention of returning the product or advising others against purchasing it. Negative sentiments should dominate the review, with little to no positive remarks, and goes beyond just mild criticism.


""" + prompt
        prompt = prompt[0:-7]
        prompt += """Choose from the options above. Do not explain your answer. Do not include any punctation. 

Answer:"""
        # print(prompt)
       
        rating = row['Rating']
        response = get_completion(prompt)
        # print(response)
        labels.append({'ID': ctr+1, 'Rating': rating, 'Label': response}) 
        print(f"{ctr+1},{rating},{response}")
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