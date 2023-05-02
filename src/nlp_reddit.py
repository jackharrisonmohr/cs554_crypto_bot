'''
Given a csv file of crypto-related Reddit posts, analyze the sentiment and append sentiment in a new column. 

Many models to choose from. 
- Trying the new 'cryptoBERT' model: https://huggingface.co/ElKulako/cryptobert?text=%2B100+Transactions+in+the+last+hour%21+Buy+your+favourite+World+Cup+team+on+the+blockchain%21 
- It could be good to compare to other models. Textblob, Vader, Pattern, SpaCy, are apparently good options.

ChatGPT code-generation prompt: 

I'm going to use the cryptoBERT model. 
Please write a Python script that:
- takes a csv file of Reddit posts, 
- analyzes the sentiment of each post with the cryptobert model, 
- appends the sentiment prediction for the post in 2 new columns: 
    -> column 1: predicted category ('Bullish', 'Neutral', or 'Bearish')
    -> column 2: confidence of prediction (between 0 and 1)

csv files have the following format (but no header line): URL, timestamp, score, author, title, selftext (post body).
Only use the title and post body for sentinment analysis.

Example usage of cryptoBERT: 

from transformers import TextClassificationPipeline, AutoModelForSequenceClassification, AutoTokenizer
model_name = "ElKulako/cryptobert"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels = 3)
pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, max_length=64, truncation=True, padding = 'max_length')
# post_1 & post_3 = bullish, post_2 = bearish
post_1 = " see y'all tomorrow and can't wait to see ada in the morning, i wonder what price it is going to be at. 😎🐂🤠💯😴, bitcoin is looking good go for it and flash by that 45k. "
post_2 = "  alright racers, it’s a race to the bottom! good luck today and remember there are no losers (minus those who invested in currency nobody really uses) take your marks... are you ready? go!!" 
post_3 = " i'm never selling. the whole market can bottom out. i'll continue to hold this dumpster fire until the day i die if i need to." 
df_posts = [post_1, post_2, post_3]
preds = pipe(df_posts)
print(preds)

output: [{'label': 'Bullish', 'score': 0.8734585642814636}, {'label': 'Bearish', 'score': 0.9889495372772217}, {'label': 'Bullish', 'score': 0.6595883965492249}]

'''

import pandas as pd
from transformers import TextClassificationPipeline, AutoModelForSequenceClassification, AutoTokenizer
from tqdm import tqdm
import sys

def do_nlp(csv_path, csv_output_path):
    # Define the model and tokenizer
    model_name = "ElKulako/cryptobert"
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)
    pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, max_length=64, truncation=True, padding='max_length')

    # Define the path to the input CSV file and output CSV file

    # Read in the CSV file
    df = pd.read_csv(csv_path, header=None, names=['url', 'timestamp', 'score', 'author', 'title', 'selftext'])

    # Combine the title and selftext columns into a single column for sentiment analysis
    df['text'] = df['title'].fillna('') + ' ' + df['selftext'].fillna('')

    # Drop the original title and selftext columns
    df = df.drop(['title', 'selftext'], axis=1)

    # Define lists to store the predicted labels and scores for each post
    labels = []
    scores = []

    # Loop through each post in the DataFrame and predict its sentiment
    for post in tqdm(df['text']):
        pred = pipe(post)[0]
        labels.append(pred['label'])
        scores.append(pred['score'])

    # Add the predicted labels and scores as new columns to the DataFrame
    df['predicted_category'] = labels
    df['confidence'] = scores

    # Save the updated DataFrame to a new CSV file
    df.to_csv(csv_output_path, index=False)

if __name__ == "__main__": 
    # Define the path to the input CSV file and output CSV file
    # csv_path = '/home/ubuntu/myraidstorage/cryptobot_cs554_project/reddit/submissions/updated_clean_data/RS_2018-03-cleaned_updated.csv'
    # csv_output_path = '/home/ubuntu/myraidstorage/cryptobot_cs554_project/reddit/submissions/reddit_sentiment_analyses/RS_2018-03_updated_sentiment.csv'
    # If calling from CLI with args
    if (len(sys.argv) > 1): 
        csv_path = sys.argv[1]
        csv_output_path = sys.argv[2]
    do_nlp(csv_path, csv_output_path)
