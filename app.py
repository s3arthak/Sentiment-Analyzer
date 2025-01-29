import re
from textblob import TextBlob
from flask import Flask, render_template, request
from ntscraper import Nitter

app = Flask(__name__)
app.static_folder = 'static'

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    
def get_tweet_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity == 0:
        return "neutral"
    else:
        return "negative"

def get_tweets(username, count=5):
    scraper = Nitter()
    tweets = scraper.get_tweets(username, mode='user', number=count)
    parsed_tweets = []

    for tweet in tweets['tweets']:
        parsed_tweet = {}
        parsed_tweet['text'] = tweet['text']
        parsed_tweet['sentiment'] = get_tweet_sentiment(parsed_tweet['text'])
        parsed_tweets.append(parsed_tweet)

    return parsed_tweets

    
# input tweet
@app.route('/')
def home():
    return render_template("index.html")

@app.route("/predict", methods=['POST', 'GET'])
def pred():
    if request.method == 'POST':
        username = request.form['query']
        count = 5  
        fetched_tweets = get_tweets(username, count)
        return render_template('result.html', result=fetched_tweets)

# for input text 
@app.route("/predict1", methods=['POST', 'GET'])
def pred1():
    if request.method == 'POST':
        text = request.form['txt']
        blob = TextBlob(text)
        if blob.sentiment.polarity > 0:
            text_sentiment = "positive"
        elif blob.sentiment.polarity == 0:
            text_sentiment = "neutral"
        else:
            text_sentiment = "negative"
        return render_template('result1.html', msg=text, result=text_sentiment)

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')




  
