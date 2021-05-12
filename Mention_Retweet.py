# Importing modules
import tweepy
import datetime
from decouple import config
import logging

# logging config
logging.basicConfig(level=logging.INFO, filename='data.txt',)
logger = logging.getLogger()


# Keys
CONSUMER_KEY = config('Consumer_Key')
CONSUMER_SECRET_KEY = config('Consumer_Secret_Key')
ACCESS_TOKEN = config('Access_Token')
ACCESS_TOKEN_SECRET = config('Access_Token_Secret')
# Authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
userID = "Aritraroy24Roy"

def get_date_list(tweets):
    # Getting tweet date-time
    date_list1 = []
    for tweet in (tweets):
        created_date = (str(tweet.created_at)).split("+")[0]
        created_date = datetime.datetime.strptime(created_date, '%Y-%m-%d %H:%M:%S')
        date_list1.append(created_date)

    # Getting date-time now    
    date_now = str(datetime.datetime.now())
    date_now = date_now.split(".")
    date_now = datetime.datetime.strptime(date_now[0], '%Y-%m-%d %H:%M:%S')
    # Getting minute diff of tweet timing and now
    final_minute_list = []
    for i in date_list1:
        result = i - date_now
        result = str((round((result.total_seconds())/60)))
        # print(result)
        first_result = result.split(" ")[0]
        final_result = first_result.split("-")[1]
        final_minute_list.append(final_result)
    return final_minute_list

def get_id_list(date_list, mentions):
    # Getting tweet text
    new_list = []
    for minute, tweet in zip(date_list, mentions):
        if "@Aritraroy24Roy" in tweet.full_text and int(minute) <= 1440:
            new_list.append(tweet.id)
    return new_list

def auto_tweet(id_list):
    # Reposting the tweet
    for id in id_list:
        try:
            api.retweet(id)
            logger.info(f"Retweet done at : {str(datetime.datetime.now())}\n\n\n")

        except Exception as e:
            logger.info(f"Retweet can't be done at : {str(datetime.datetime.now())} due to {e} error\n\n\n")

if __name__=='__main__':
    mentions = api.mentions_timeline(tweet_mode='extended')
    minute_list = get_date_list(mentions)
    id_list = get_id_list(minute_list, mentions)
    auto_tweet(id_list)
    logger.info(f"Ran at : {str(datetime.datetime.now())}\n==================   *****   =================\n")