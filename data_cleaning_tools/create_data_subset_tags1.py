import csv

def filter_and_write_csv(input_csv, output_csv, filter_field, columns):
    # List to store filtered rows
    filtered_rows = []

    # Read the input CSV file and filter rows
    with open(input_csv, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            filter_value = row[filter_field]
            if filter_value and filter_value != 'REMOVE' and filter_value != "0" and filter_value != "":
                filtered_row = {column: row[column] for column in columns}
                #filtered_row[filter_field] = filter_value

                design = row['design']
                value = row['value']
                performance = row['performance']
                quality = row['quality']
                none = row['none']
                nonreview = row['non-review']

                #format tags here as desired, overwrite the tags field in filtered_row

                filtered_row['tags'] = ""
                if design == "1":
                    filtered_row['tags'] += '"design"'
                if performance == "1":
                    if filtered_row['tags'] != "":
                        filtered_row['tags'] += ","
                    filtered_row['tags'] += '"performance"'
                if quality == "1":
                    if filtered_row['tags'] != "":
                        filtered_row['tags'] += ","
                    filtered_row['tags'] += '"quality"'
                if value == "1":
                    if filtered_row['tags'] != "":
                        filtered_row['tags'] += ","
                    filtered_row['tags'] += '"value"'
                if none == "1":
                    filtered_row['tags'] += '"none"'
                if nonreview == "1":
                    filtered_row['tags'] += '"non-review"'


                filtered_row['tags'] = "[" + filtered_row['tags']  +  "]"
                filtered_rows.append(filtered_row)

    # Write filtered rows to a new CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = columns
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)

# Example usage:
input_csv_path = 'external/ReviewTags_v1.csv'
output_csv_path = 'external/ReviewTags_v1_set1.csv'
filter_field = 'tags'
columns = ['product_name', 'review_text', 'tags']

filter_and_write_csv(input_csv_path, output_csv_path, filter_field, columns)

