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


input_file = '/home/ubuntu/myraidstorage/cryptobot_cs554_project/reddit/submissions/uncompressed_zsts/RS_2018-01'
output_file = '/home/ubuntu/myraidstorage/cryptobot_cs554_project/reddit/submissions/relevant_posts/RS_2018-01_relevant_posts.csv'
import json
import csv
import re

# Set of relevant keywords to filter for
keywords = {'crypto', 'cryptocurrency', 'bitcoin', 'btc', 'blockchain', 'eth', 'ethereum', 'ripple', 'xrp', 'altcoin', 'litecoin', 'LTC'}

# Function to clean and extract relevant information from a post
def clean_post(post):
    cleaned = {}
    cleaned['permalink'] = 'https://www.reddit.com' + post['permalink']
    cleaned['created_utc'] = post['created_utc']
    cleaned['score'] = post['score']
    cleaned['author'] = post['author']
    cleaned['title'] = post['title']
    cleaned['selftext'] = post['selftext']
    return cleaned

# Function to write the cleaned posts to a CSV file
def write_csv(posts, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['permalink', 'created_utc', 'score', 'author', 'title', 'selftext'])

        for post in posts:
            # Escape any double quotes that are already in the fields
            title = post['title'].replace('"', '""')
            selftext = post['selftext'].replace('"', '""')

            # Enclose the title and selftext fields in quotes to handle commas and other special characters
            writer.writerow([post['permalink'], post['created_utc'], post['score'], post['author'], f'"{title}"', f'"{selftext}"'])

# Open the input file and filter for relevant posts
with open(input_file, 'r', encoding='utf-8') as input_file:
    posts = []
    for line in input_file:
        post = json.loads(line)
        if any(keyword in post['title'].lower() or keyword in post['selftext'].lower() for keyword in keywords):
            cleaned_post = clean_post(post)
            posts.append(cleaned_post)

# Remove duplicates
posts = [dict(t) for t in {tuple(d.items()) for d in posts}]

# Sort by created_utc
posts = sorted(posts, key=lambda k: k['created_utc'])

# Write to CSV file
write_csv(posts, output_file)
