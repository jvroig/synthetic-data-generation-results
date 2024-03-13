import csv
import random
import jsonlines
import data_augmentation_tools as augment

# # Define the list of augmentation functions to apply
# augmentation_functions = [
#     augment.random_char_insertion,
#     augment.random_char_removal,
#     augment.random_char_replacement,
#     augment.random_adjacent_swap,
#     augment.random_word_deletion,
#     augment.random_word_insertion,
#     augment.random_word_replacement,
#     augment.random_sentence_deletion,
#     augment.random_word_shuffle,
#     augment.synonym_replacement,
#     augment.expand_contractions,
#     augment.noise_injection,
#     augment.back_translation_augmentation,
#     augment.keyboard_typos_simulation,
#     augment.text_duplication,
# ]

split = "train"
do_augmentation = True
input_csv_path = 'processed_' + split + '.csv'
output_jsonl_path = 'dataset_' + split + '.jsonl'

# Lookup table for converting original sentiment to final sentiment
sentiment_conversion = {
    'strongly positive': 'Positive',
    'mostly positive': 'Positive',
    'slightly positive': 'Slightly Positive',
    'mixed but leans positive': 'Slightly Positive',
    'strongly negative': 'Negative',
    'mostly negative': 'Negative',
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
- Positive
- Slightly Positive
- Negative
- Slightly Negative

What is the overall sentiment of that product review?

Choose from the options above. Do not explain your answer. Do not include any punctation.

Answer:"""

    return prompt_string.strip(), final_sentiment

        
def process_csv(input_csv, output_jsonl, do_augmentation=False):
    with open(input_csv, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        data = []
        for row in reader:
            product_name = row['product_name']
            review_text = row['review_text']
            sentiment = row['sentiment']
            
            prompt_string, answer = generate_prompt(product_name, review_text, sentiment)
            data.append({'prompt': prompt_string, 'completion': answer})

            if(do_augmentation):
                #Data augmentation
                augmented_reviews = augment.apply_augmentations(review_text)
                for augmented_review in augmented_reviews:
                    prompt_string, answer = generate_prompt(product_name, augmented_review, sentiment)
                    data.append({'prompt': prompt_string, 'completion': answer})

    with jsonlines.open(output_jsonl, 'w') as writer:
        # Shuffle the dataset if desired
        random.seed()
        random.shuffle(data)
        for item in data:
            writer.write(item)


process_csv(input_csv_path, output_jsonl_path, do_augmentation=do_augmentation)
