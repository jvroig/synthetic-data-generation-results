import csv

# Replace 'input_csv_path' and 'output_csv_path' with actual file paths
input_csv_path = 'expid_2024-02-25/processed_output.csv'
output_csv_path = 'dataset.csv'


# Lookup table for converting original sentiment to final sentiment
sentiment_conversion = {
    'strongly positive': 'Strongly Positive',
    'mostly positive': 'Strongly Positive',
    'slightly positive': 'Slightly Positive',
    'mixed but leans positive': 'Slightly Positive',
    'strongly negative': 'Strongly Negative',
    'mostly negative': 'Strongly Negative',
    'slightly negative': 'Slightly Negative',
    'mixed but leans negative': 'Slightly Negative'
}

def generate_prompt(product_name, review_text, sentiment):
    final_sentiment = sentiment_conversion.get(sentiment.lower().strip(), 'Unknown')  # Convert 
    prompt_string = f"""
Here is a product review from a customer, which is delimited with triple backticks.

Product Name: {product_name}
Review text: 
```
{review_text}
```

Overall sentiment must be one of the following options:
- Strongly Positive
- Slightly Positive
- Strongly Negative
- Slightly Negative

What is the overall sentiment of that product review?

Answer:"""

    return prompt_string.strip(), final_sentiment

def process_csv(input_csv, output_csv):
    with open(input_csv, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        data = []
        for row in reader:
            product_name = row['product_name']
            review_text = row['review_text']
            sentiment = row['sentiment']
            
            prompt_string, answer = generate_prompt(product_name, review_text, sentiment)
            data.append({'text': prompt_string, 'answer': answer})
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['text', 'answer']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in data:
            writer.writerow(item)

process_csv(input_csv_path, output_csv_path)
