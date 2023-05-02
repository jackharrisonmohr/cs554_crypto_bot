import csv
import sys
def update(input_file, output_file): 
    # Define keywords to keep
    keywords = ['bitcoin', 'crypto', 'cryptocurrency', 'btc', 'blockchain', 'ethereum']

    # Define function to truncate selftext if necessary
    def truncate(text):
        if len(text) > 300:
            return text[:300] + '...'
        else:
            return text

    # Read input CSV file and filter entries
    with open(input_file, 'r') as f_in:
        reader = csv.reader(f_in)
        data = [row for row in reader if any(keyword in row[4].lower() for keyword in keywords)]

    # Truncate selftext if necessary
    data = [[row[0], row[1], row[2], row[3], row[4], truncate(row[5])] for row in data]

    # Sort data by timecode
    data = sorted(data, key=lambda x: x[1])

    # Write output CSV file
    with open(output_file, 'w', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerows(data)

if __name__ == "__main__": 
    # Define input and output filenames
    input_file = '/home/ubuntu/myraidstorage/cryptobot_cs554_project/reddit/submissions/process_these/RS_2019-04.zst.ndjson.csv'
    output_file = '/home/ubuntu/myraidstorage/cryptobot_cs554_project/reddit/submissions/process_these/RS_2019-04_v2.csv'
    #if calling from CLI with args. 

    update(input_file, output_file)