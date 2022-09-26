import tweepy
import pprint
import re
from collections import defaultdict, OrderedDict, namedtuple


def update_data(current: str, next: str, data: dict):
    '''
    Populates the lexicon. Each word points to an OrderedDict of words so that
    the algorithm can prioritize date if counts for multiple next words are the same.
    '''
    if current in data:
        if next in data[current].keys():
            data[current][next] += 1
        else:
            data[current][next] = 1
    else:
        data[current] = OrderedDict([(next,1)])


def get_user_data(client, user: str, limit: int):
    '''
    Returns a lexicon derived from a specified number of tweets of a specified username.
    '''
    user_id = client.get_user(username = user).data.id

    data: dict = {}
    paginator = tweepy.Paginator(client.get_users_tweets, id = user_id, exclude = "retweets", limit = limit)
    for tweets in paginator:
        for tweet in tweets.data:
            tweet = re.sub(r'https://t.co/[\w]*',"", tweet.text)
            words = re.findall(r"[a-zA-Z]+’?[a-zA-Z]*", tweet)
            for i in range(len(words)-1):
                update_data(words[i], words[i+1], data)
    return data



