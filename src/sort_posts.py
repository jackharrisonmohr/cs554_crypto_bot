# Open CSV file and sort by created_utc in ascending order
with open(output_file, 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    sorted_posts = sorted(reader, key=lambda row: int(row[1]))

# Write sorted data back to CSV file
with open('relevant_posts.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(sorted_posts)