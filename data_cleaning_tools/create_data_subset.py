import csv

def filter_and_write_csv(input_csv, output_csv, filter_field, columns):
    # List to store filtered rows
    filtered_rows = []

    # Read the input CSV file and filter rows
    with open(input_csv, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            filter_value = row[filter_field]
            if filter_value and filter_value != 'REMOVE':
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
input_csv_path = '../external/v4_labels_processed.csv'
output_csv_path = '../external/v4_test_set4.csv'
filter_field = 'Test Set 4 Labels'
columns = ['ID', 'Prompt_Text', 'Test Set 4 Labels']

filter_and_write_csv(input_csv_path, output_csv_path, filter_field, columns)

