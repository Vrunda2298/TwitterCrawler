# TwitterCrawler

## CONFIGURATION REQUIREMENT
* Python 3.9
* Packages listed below needs to be added for project to execute successfuly

## COMPILATION & EXECUTION
* Add your twitter keys and tokens in const.py file.
* Run the main.py file.
* And the code will display the profile information for a list of users, friends and first 20 followers of users, first 50 tweets that contains keywords [Ohio, weather] and first 50 tweets that originates from Dayton region.
* Additionally, it performs Sentiment Analysis on the 5 e-Commerce companies and send the first 20 positive and negative tweets of the company having maximum positive tweets to the provided email address.

## INFORMATION
➢ This project has following two files:
   * main.py
   * const.py

### • Brief description on two files:
➢ main.py: the main file has following functions,
  * main(): that has a list of user’s screen names and prints the user’s profile
information, friends and followers.
  * profile_info(): returns user’s profile information .
  * valid_input(): checks whether the username is valid twitter username or not.
  * get_friends_list(): that generates a list of user’s friends on twitter.
  * get_followers_list(): that generates a list of user’s followers on twitter.
  * get_tweets_by_keyword(): that prints the first 50 tweets that contains keywords
[Ohio, weather].
  * get_tweets_by__location(): that prints first 50 tweets that originates from Dayton
region.
  * clean_tweet(): cleans the tweets.
  * get_tweets_for_comapny(): retrieves the first 1000 public tweets of the 5
companies and perform sentiment analysis on it, to get the number of positive and
negative tweets.
  * get_sentiment(): returns whether the tweet is positive or negative by checking the
polarity using TextBlob library.

➢ const.py:
- This file contains four variables namely:
  * CONSUMER_KEY
  * CONSUMER_SECRET
  * ACCESS_TOKEN
  * ACCESS_TOKEN_SECRET
