import csv
import data_augmentation_tools as augment

# Define the list of augmentation functions to apply
augmentation_functions = [
    augment.random_char_insertion,
    augment.random_char_removal,
    augment.random_char_replacement,
    augment.random_adjacent_swap,
    augment.random_word_deletion,
    augment.random_word_insertion,
    augment.random_word_replacement,
    augment.random_word_shuffle,
    augment.synonym_replacement,
    augment.expand_contractions,
    augment.noise_injection,
    augment.back_translation_augmentation,
    augment.keyboard_typos_simulation,
    augment.text_duplication,
]

# Input and output file paths
input_csv_path = 'input.csv'
output_csv_path = 'output.csv'

# Function to apply augmentations to a string
def apply_augmentations(input_string):
    augmented_strings = []
    for func in augmentation_functions:
        augmented_strings.append(func(input_string))
    return augmented_strings

# Read input CSV file and apply augmentations to each row
with open(input_csv_path, 'r', newline='', encoding='utf-8') as input_file:
    reader = csv.DictReader(input_file)
    rows = list(reader)
    header = reader.fieldnames

    # Add augmented fields to the header
    augmented_header = header + [func.__name__ for func in augmentation_functions]

    # Apply augmentations to each row
    augmented_rows = []
    for row in rows:
        augmented_row = row.copy()
        input_string = row['text']  # Assuming 'text' is the column containing strings to augment
        augmented_strings = apply_augmentations(input_string)
        for i, augmented_string in enumerate(augmented_strings):
            augmented_row[augmentation_functions[i].__name__] = augmented_string
        augmented_rows.append(augmented_row)

# Write augmented data to output CSV file
with open(output_csv_path, 'w', newline='', encoding='utf-8') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=augmented_header)
    writer.writeheader()
    writer.writerows(augmented_rows)

print("Data augmentation complete. Output saved to:", output_csv_path)
