import csv
import random
import os


# Replace 'input_csv_path' and output file paths with desired paths
input_csv_path = 'expid_2024-02-25/processed_output.csv'
output_train_path = 'processed_train.csv'
output_eval_path = 'processed_eval.csv'
output_test_path = 'processed_test.csv'


train_ratio      = 0.90
eval_ratio       = 0.05
test_ratio       = 0.05

#Specifying fixed sizes for a set will override the ratio for it
fixed_train_size = 0 #Useful if you want a specific number for your dataset
#fixed_eval_size  = 0 #Might be a future feature
#fixed_test_size  = 0 #Might be a future feature


def split_dataset(input_csv, output_train, output_eval, output_test, train_ratio=train_ratio, eval_ratio=eval_ratio, test_ratio=test_ratio, shuffle_dataset=True, random_seed=None):
    if not os.path.exists(input_csv):
        print(f"Error: Input CSV file '{input_csv}' does not exist.")
        return

    if not (0 <= train_ratio <= 1) or not (0 <= eval_ratio <= 1) or not (0 <= train_ratio + eval_ratio <= 1):
        print("Error: Invalid split ratios.")
        return

    # Read the dataset from input CSV file
    dataset = []
    with open(input_csv, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dataset.append(row)

    # Shuffle the dataset if desired
    if shuffle_dataset:
        #Create random seed, or use specified seed if given
        if random_seed == None:
            random.seed()
        else:
            random.seed(random_seed)

        random.shuffle(dataset)

    # Calculate sizes for each split
    total_size = len(dataset)
    if fixed_train_size > 0:
        train_size = fixed_train_size
        remaining_size = total_size - train_size
        percent_remaining = eval_ratio + test_ratio
        eval_ratio = eval_ratio / percent_remaining
        test_ratio = test_ratio / percent_remaining
        eval_size = int(eval_ratio * remaining_size)
        test_size = total_size - train_size - remaining_size
    else:
        train_size = int(train_ratio * total_size)
        eval_size = int(eval_ratio * total_size)
        test_size = total_size - train_size - eval_size

    # Split the dataset
    train_data = dataset[:train_size]
    eval_data = dataset[train_size:train_size + eval_size]
    test_data = dataset[train_size + eval_size:]

    # Write to output CSV files
    write_to_csv(output_train, train_data)
    write_to_csv(output_eval, eval_data)
    write_to_csv(output_test, test_data)

def write_to_csv(output_csv, data):
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = list(data[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

split_dataset(input_csv_path, output_train_path, output_eval_path, output_test_path)
