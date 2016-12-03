# twitterBot.py
# Class Project for CPSC 353, where we make a Twitter Bot that retweets popular tweets from popular topics.
# Refer to https://dev.twitter.com/rest/reference for methods usage
# https://github.com/sixohsix/twitter for the type of API we're using
# Authors: Matthew Shiroma and Ryan Britton
# Version 1.0
import twitter
import logging
import json
import random
from urllib import unquote
import time

# In order to use the Twitter API, we need to authenticate ourselves.
def retweet():
    CONSUMER_KEY = 'zjxEmYxGwIHUYLhT9RicrVRNv'
    CONSUMER_SECRET = 'fvqPvStA7SF3Ai9pv8zraK5M2aZtfEtF5PkEr8smit9PmLkTE3'
    OAUTH_TOKEN = '773755889107042305-WOaFeB3FiK7xvPg1LZQmFUM7uABgasy'
    OAUTH_TOKEN_SECRET = 'v1KAZgsHYXvBot3cIeocEKmKe36MoFmG7BvBpe8EJgJWo'
    WORLD_WOE_ID = 1
    US_WOE_ID = 23424977

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)

    # We now get the trends from the world and the US and compare them to see where they overlap to find the most popular trend.
    world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
    us_trends = twitter_api.trends.place(_id=US_WOE_ID)

    world_trends_set = set([trend['name']
                            for trend in world_trends[0]['trends']])

    us_trends_set = set([trend['name']
                         for trend in us_trends[0]['trends']])

    # We get the popular trends right now in a set.
    common_trends = world_trends_set.intersection(us_trends_set)
    print "Here's the top trends: "
    print common_trends

    # In order to get a "random" top trend, we first pop off the first trend and generates a random number using the
    # length of the set. If it's not 0, a new trend will be found by iterating through the set X numb of times
    # X = rand
    numbTweets = 1000
    top_trend = str(common_trends.pop())
    rand = random.randrange(0,len(common_trends))

    if(rand != 0):
        while(rand > 0):
            top_trend = str(common_trends.pop())
            rand = rand - 1

    print "The top trend that's choosen is: "
    print top_trend

    # We then search through 1000 tweets using that top trend. We then only take the status part of the search, which is
    # the list of tweets that contain the top trend. This is a Dictionary object
    search_results = twitter_api.search.tweets(q=top_trend, count=numbTweets)
    statuses = search_results['statuses']

    # Likes/Retweet Solution: We look through the results to find statuses that have more than 100 retweets/favorites on it.
    # If it does, we then access the original tweet (if it's a retweet) from it and putting it into a list.
    # Else, we simply put that tweet into the list.

    modified_results = []
    for curr_tweet in statuses:
        if(curr_tweet.get('retweet_count') > 100 or curr_tweet.get('favorite_count') > 100):
            if(curr_tweet.get('retweeted_status') != None):
                print("Tweet was a retweet.")
                orig_tweet = curr_tweet.get('retweeted_status')
                print(orig_tweet.get('text'))
                print(orig_tweet.get('favorite_count'))
                print(orig_tweet.get('retweet_count'))

                if(orig_tweet not in modified_results):
                    modified_results.append(orig_tweet)
                    print("Added tweet into list")

            else:
                print("Tweet was an ORIGINAL tweet")
                print(curr_tweet.get('text'))
                print(curr_tweet.get('favorite_count'))
                print(curr_tweet.get('retweet_count'))

                if(curr_tweet not in modified_results):
                    modified_results.append(curr_tweet)
                    print("Added tweet into list")
            print

    # From here, we look through the list we made and see which tweet has the greatest amount of likes and retweets. Once
    # we find one, we store it for later use. Favorite count preceeds over retweet count.
    most_liked_amount = 0
    most_retweeted_amount = 0
    popular_tweet = None
    for curr_tweet in modified_results:
        if(curr_tweet.get('favorite_count') > most_liked_amount and curr_tweet.get('retweet_count') > most_retweeted_amount):
            popular_tweet = curr_tweet
            most_liked_amount = curr_tweet.get('favorite_count')
            most_retweeted_amount = curr_tweet.get('retweet_count')
        elif(curr_tweet.get('favorite_count') > most_liked_amount):
            popular_tweet = curr_tweet
            most_liked_amount = curr_tweet.get('favorite_count')
        elif(curr_tweet.get('retweet_count') > most_retweeted_amount):
            popular_tweet = curr_tweet
            most_retweeted_amount = curr_tweet.get('retweet_count')

    if(popular_tweet != None):
        print("Most popular tweet is: ")
        print(popular_tweet.get('text'))
        print(popular_tweet.get('favorite_count'))
        print(popular_tweet.get('retweet_count'))

    # Sentiment analysis solution: Analyse all of the tweets gotten through the top trend by first, extracting all of the
    # words from a tweet, and analyzing their sentiment value. The highest sentiment score along with the tweet that has it
    # will be saved after the main analysis loop is done.

    # We convert the file into a usable format.
    sentiment_word_file = open('AFINN-111.txt')
    sentiment_word_scores = {}
    for line in sentiment_word_file:
        term, score  = line.split("\t")
        sentiment_word_scores[term] = int(score)

    # We analyze the tweets we've gotten using the score dictionary we created.
    highest_score = 0
    associated_tweet = None
    for curr_tweet in modified_results:

        # We extract out the individual words in the tweet.
        words_in_tweet = curr_tweet.get('text').split()

        #  Using the score file, we grade the tweet by seeing if it has key words.
        tweet_sentiment = 0
        for curr_word in words_in_tweet:
            uword = curr_word.encode('utf-8')
            if uword in sentiment_word_scores.keys():
                tweet_sentiment = tweet_sentiment + sentiment_word_scores[curr_word]

        # We then store the tweet along with its score in a variable if its sentiment value beats he highest one.
        if(tweet_sentiment > highest_score):
            highest_score = tweet_sentiment
            associated_tweet = curr_tweet

    if(associated_tweet != None):
        print("The tweet that receive the highest score was ")
        print(associated_tweet.get('text'))
        print(associated_tweet.get('favorite_count'))
        print(associated_tweet.get('retweet_count'))
        print(highest_score)
        new_tweet = associated_tweet
        publish = True
        if new_tweet.get('lang') and new_tweet.get('lang') != 'en':
            publish = False
        else:
            for i in range(0, 16): ## iterate through 16 times to get max No. of tweets
                name = twitter_api.account.verify_credentials()
                user_timeline = twitter_api.statuses.user_timeline(user_id=name.get('id_str'),count=200)
                for tweet in user_timeline:
                    if (tweet.get('id') == new_tweet.get('id')):
                        publish = False
        if publish:
            twitter_api.statuses.retweet(id=tweet.get('id'))
            logging.debug("RT: {}".format(tweet['text']))


    time.sleep(20)



while True:
    retweet()
# tweetNumb = random.randrange(0,len(statuses))
# selected_tweet_ID = statuses[tweetNumb].get('id')
# print("The selected tweet's ID is: ")
# print(selected_tweet_ID)
# testStatus = twitter_api.statuses.update(status="I FINALLY DID IT!")
# print json.dumps(testStatus, indent=1)
# testStatus = twitter_api.statuses.retweet(id=selected_tweet_ID)
print "End of Program!"
