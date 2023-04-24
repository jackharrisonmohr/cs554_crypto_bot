'''

Step 1: prep the Reddit dataset:
- For each zst file in the Reddit torrent: 
    -> download the file
    -> uncompress the file with zstd
    -> clean the uncompressed ndjson file and write the output to a new csv
        -> only add posts relevant to crypto (use a set of keywords to filter for only posts that contain one of the keywords in their title or body text)
        -> Add each post in the following format: permalink, created_utc, score, author, title, selftext
        -> after you've added all the relevant posts: 
            -> remove duplicates
            -> sort by created_utc
- Test the above with one file, then write script to do the rest of them automatically.
- Try appending all the resulting csv's to one main csv. This may or may not be good depending on size. 

Step 2: do sentiment analysis on Reddit dataset: 
- Use a Python library to analyze the sentiment of each post
- Create a new csv file that is a time series with the following values: day, crypto_sentiment, crypto_post_volume

Step 3: train model 
- Use BTC price time series and the reddit_crypto_sentiment time series to train a binary classifier

Step 4: test model (and compare to baseline)





Additional features to consider adding later:
- get posts about the stock market and finance as well
- also get reddit comments
- Try improving model by adding bitcoin price time series
- Change model from binary classifier to numerical prediction, to predict the price change not just the direction

'''

import json
import csv
input_file = '/home/ubuntu/myraidstorage/cryptobot_cs554_project/reddit/submissions/uncompressed_zsts/RS_2018-01'
output_file = '/home/ubuntu/myraidstorage/cryptobot_cs554_project/reddit/submissions/relevant_posts/RS_2018-01_relevant_posts.csv'
# Set of relevant keywords to filter posts
keywords = {'bitcoin', 'crypto', 'cryptocurrency', 'btc', 'blockchain', 'ethereum', }

# Open input ndjson file
with open(input_file, 'r') as f:

    # Open output CSV file for writing
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:

        # Create CSV writer object
        writer = csv.writer(csv_file)

        # Create set to store post IDs to remove duplicates
        post_ids = set()

        # Iterate over each line (post) in the ndjson file
        for line in f:

            # Parse the line as JSON
            post = json.loads(line)

            # Check if post title or body text contains any of the relevant keywords
            if any(keyword in post['title'].lower() or keyword in post['selftext'].lower() for keyword in keywords):

                # Check if post ID is already in set to remove duplicates
                if post['id'] not in post_ids:

                    # Add post to set of IDs
                    post_ids.add(post['id'])

                    # Write relevant post data to CSV file
                    writer.writerow([post['permalink'], post['created_utc'], post['score'], post['author'], post['title'], post['selftext']])

# Open CSV file and sort by created_utc in ascending order
with open('relevant_posts.csv', 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    sorted_posts = sorted(reader, key=lambda row: int(row[1]))

# Write sorted data back to CSV file
with open('relevant_posts.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(sorted_posts)