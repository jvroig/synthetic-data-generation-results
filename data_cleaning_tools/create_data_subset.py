import csv

def filter_and_write_csv(input_csv, output_csv, filter_field, columns):
    # List to store filtered rows
    filtered_rows = []

    # Read the input CSV file and filter rows
    with open(input_csv, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            filter_value = row[filter_field]
            if filter_value and filter_value != 'REMOVE' and filter_value != "0":
                filtered_row = {column: row[column] for column in columns}
                filtered_row[filter_field] = filter_value
                filtered_rows.append(filtered_row)

    # Write filtered rows to a new CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = columns
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)

# Example usage:
input_csv_path = 'external/SentiV3_var1541_train_scored.csv'
output_csv_path = 'external/v3B_test_set2.csv'
filter_field = 'Set 2 Labels'
columns = ['prompt','Set 2 Labels']

filter_and_write_csv(input_csv_path, output_csv_path, filter_field, columns)

