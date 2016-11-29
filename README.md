# DrumpfBot
Our class project for CPSC 353 will be to create a Twitter program using the basis of the Sentiment Analysis project we made earlier and add on more features. We are planning to make a “Twitter Bot” (a Twitter user that is controlled by a computer rather than a person) that will analyze the sentiment stream every 20 minutes. After every analysis, it will determine which hashtag is the most liked out of all of the tweets it found. Once it finds the most positive post with said popular hashtag and retweet it.

## Goal for Next Submission
- Create a Twitter account that will host the program retweets.
- Code the part of program that will periodically retweet tweets.

### Participants and Roles
* Matthew Shiroma: Coding finding tweets using a random trend and filtering through them to find a tweet with the highest sentiment score.
* Ryan Britton: Coding part of program that will periodically retweet tweets and (tenative) making a simple text based UI for program.

### Concepts used in Class
-	Connecting to a server and searching its database.
-	Using Github.
-	Understanding the Sentiment Analysis project.
-	Creating an Application that will “hide” the underlining layers of the network layers.

### How to Run Program
1. You can either download this twitter API from [this GitHub repository](https://github.com/sixohsix/twitter) or you can make a ssh connection to icd.chapman.edu, since that already has this API installed.
2. Clone the repository from the master branch onto your computer or in the icd.chapman.edu server, depending if you installed the API on your own device.
3. Run TwitterBot.py by typing in “python TwitterBot.py”.
4. The program will display the top trends, the tweets with more than 100 likes/retweets, and the tweet that has the most likes/retweets. The second part will then display the tweet that has the highest sentiment score. That tweet will be the one that is retweeted.
5. To check if the programmed retweeted that tweet, go to [this Twitter page](https://twitter.com/drumpfbot2016) to find the retweet. If nothing is on there, it was either because there isn't a tweet that was over 100 likes or retweets, or there wasn't a tweet with a positive sentiment score.
