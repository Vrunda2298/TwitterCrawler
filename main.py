import const
import tweepy
from tweepy import Stream
import math
from textblob import TextBlob
import re
import smtplib, ssl
from email.message import EmailMessage


followers_list = []
friends_list = []
followers_screen_names = []

# A listener handles tweets that are received from the stream.
# This is a basic listener that prints recieved tweets to standard output

class TweetListener(Stream):
    def onData(self, data):  # return data
        print(data)
        return True

    def onError(self, status):  # return status on error
        print(status)


# Check whether input is a valid username or not
def valid_input(username):
    if username is None:
        return False
    username = username.strip()
    if len(username) <= 0:
        return False
    if username.isspace():
        return False
    return True

# TASK 1
# Returns object user to get twitter's user information
def profile_info(screen_name, api):
    try:
        user = api.get_user(screen_name = screen_name)
        # print(user)
        if user is None:
            return

    except Exception as e:
        print(e)

    return user


# TASK 2
# Generates friend list for given user
def get_friends_list(screen_name, api, no_of_pages, follower_pages):
    try:
        if len(followers_list) <= 0:
            get_followers_list(screen_name, api, follower_pages)

        for page in tweepy.Cursor(api.get_friends, screen_name = screen_name, count=200).pages(no_of_pages):

            if len(page) == 0:
                break

            for p in page:
                if p.screen_name in followers_screen_names:
                    friends_list.append(p.name)
    except Exception as e:
        print(e)


# TASK 2
# Generates follower list for given user
def get_followers_list(screen_name, api, no_of_pages):
    try:
        for page in tweepy.Cursor(api.get_followers, screen_name = screen_name, count=200).pages(no_of_pages):
            # print(len(page))
            if len(page) == 0:
                break

            for p in page:
                followers_screen_names.append(p.screen_name)
                followers_list.append(p.name)

    except Exception as e:
        print(e)

    return followers_list


# TASK 3
# Prints first 50 tweets that contains two keywords [Ohio, weather]
def get_tweets_by_keyword(api):
    search_terms = "ohio weather"
    tweets = api.search_tweets(q=search_terms, count=50)    # 7-day limit on tweets
    print("\n\n----------------------------------------------------------------------------------------------------------------------------------------------------")
    print("                                           First 50 tweets that contains two keywords [Ohio, weather]")
    print("----------------------------------------------------------------------------------------------------------------------------------------------------")

    for t in tweets:
        print(t.created_at, t.user.screen_name, t.text)


# TASK 3
# Prints first 50 tweets that originates from Dayton region
def get_tweets_by_location(api, radius):
    # Coordinates for Dayton Ohio
    latitude = 39.758949
    longitude = -84.191605
    tweets = api.search_tweets(q = " ", geocode=str(latitude)+","+str(longitude)+","+radius, count=50)
    print("\n\n----------------------------------------------------------------------------------------------------------------------------------------------------")
    print("                                                First 50 tweets that originates from Dayton region")
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------")
    for t in tweets:
        print(t.created_at, t.user.screen_name, t.text)


# TASK 4
# Sentiment Analysis on 5 e-Commerce companies based on the public tweets

# Method to clean retrieved tweets
def clean_tweet(tweet):

    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+)", " ", tweet).split())

# Method to get sentiments for each tweet
def get_sentiment(tweet):

    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity >= 0:
        return 'positive'
    else:
       return 'negative'

# Method to get public tweets for the 5 e-Commerce companies: Amazon, Best Buy, eBay, Shein, Flipkart
def get_tweets_for_company(api, companies, t_data):
    try:
        for comp in companies:
            for page in tweepy.Cursor(api.search_tweets, q=comp, count=100).pages(10):
                if len(page) == 0:
                    break
                for p in page:
                    info = dict()
                    info['text'] = p.text
                    info['sentiment'] = get_sentiment(str(p.text))
                    t_data[comp].append(info)
        return t_data
    except Exception as e:
        print(e)

# Method to send an Email of Positive & Negative tweets for the best company based on Sentiment Analysis from 1000
# tweets for each company.
def send_email(t_data, company):
    msg = EmailMessage()
    message_positive = []
    message_negative = []

    p_tweets = [tweet for tweet in t_data[company] if tweet['sentiment'] == 'positive']
    for i in p_tweets:
        message_positive.append(i['text'])
        if len(message_positive) > 20:
            break

    n_tweets = [tweet for tweet in t_data[company] if tweet['sentiment'] == 'negative']
    for i in n_tweets:
        message_negative.append(i['text'])
        if len(message_negative) > 20:
            break

    message = "\n**************************************************\n"\
              +'Positive Tweets' + "\n**************************************************\n"
    message += "\n".join(message_positive)
    message += "\n\n\n**************************************************\n"+\
               'Negative Tweets' + "\n**************************************************\n"
    message += "\n".join(message_negative)
    msg.set_content(message)

    email_to = input("\n\nEnter Email ID for receiving the tweets for " + company + ": ")
    msg['Subject'] = 'Positive & Negative Tweets for the best e-Commerce Company based on Sentiment Analysis'
    msg['From'] = "patelvrunda004@gmail.com"
    msg['To'] = email_to

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("patelvrunda004@gmail.com", "patel@004")
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(e)


# main() function
def main():
    auth = tweepy.OAuthHandler(const.CONSUMER_KEY, const.CONSUMER_SECRET)
    auth.set_access_token(const.ACCESS_TOKEN, const.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print('Verification Successful.')
    except:
        print('Authentication Error.')

    twitterStream = Stream(const.CONSUMER_KEY, const.CONSUMER_SECRET, const.ACCESS_TOKEN, const.ACCESS_TOKEN_SECRET)

    # List of user's screen names
    user_screen_names = ['TommyDavis55', 'Heather60064652', 'patelvrunda27', 'NirmalaJadhav02', 'lis_bet0']

    for username in user_screen_names:

        global followers_list, friends_list, followers_screen_names
        followers_list = []
        friends_list = []
        followers_screen_names = []

        if not valid_input(username):
            return

        # Method call for TASK 1
        user = profile_info(username, api)

        no_of_frnds_pages = math.ceil(user.friends_count/200)
        no_of_followers_pages = math.ceil(user.followers_count/200)

        # Method call for TASK 2
        get_followers_list(username, api, no_of_followers_pages)

        # Method call for TASK 2
        get_friends_list(username, api, no_of_frnds_pages, no_of_followers_pages)

        print("\n\n-----------------------------------------------------------------------------------------------------------------------------------------------------")
        print("                                                         Profile Information of", username)
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------")

        print("\nUser name: ", user.name)
        print("Screen name: ", user.screen_name)
        print("User ID: ", user.id_str)
        print("Location: ", user.location)
        print("User Description: ", user.description)
        print("The number of Followers: ", user.followers_count)
        print("The number of friends: ", len(friends_list))
        print("The number of tweets: ", user.statuses_count)
        print("User URL: ", user.url)

        #print("\n")
        print("\nFirst 20 followers of", username)
        print("----------------------------------------")
        print(*followers_list[:20], sep='\n')

        #print("\n")
        print("\nFriend List of", username)
        print("----------------------------------------")
        print(*friends_list, sep='\n')

    # Method call for TASK 3
    get_tweets_by_keyword(api)

    # Method call for TASK 3
    get_tweets_by_location(api, "25mi")

    companies = ['amazon','ebay','shein','flipkart','bestbuy']
    t_data = dict()
    for i in companies:
        t_data[i] = []

    # Method call for TASK 4
    twt_data = get_tweets_for_company(api, companies, t_data)
    ptn_ratio = []

    for i in companies:
        print("\n\n-----------------------------------------------")
        print("Sentiment Analysis for", i)
        print("-----------------------------------------------")
        positive_tweets = [tweet for tweet in twt_data[i] if tweet['sentiment'] == 'positive']
        positive_percentage = round((100 * len(positive_tweets) / len(t_data[i])), 2)
        print("Percentage of Positive tweets:", positive_percentage, "%")
        negative_tweets = [tweet for tweet in twt_data[i] if tweet['sentiment'] == 'negative']
        negative_percentage = round((100 * len(negative_tweets) / len(t_data[i])), 2)
        print("Percentage of Negative tweets:", negative_percentage, "%")

        ptn_ratio.append((positive_percentage / negative_percentage))

    ind = ptn_ratio.index(max(ptn_ratio))

    for i in range(len(companies)):
        if i == ind:
            company = companies[ind]

    print("\n\nThe best company based on the sentiment analysis at the moment is", company)
    # Method call for TASK 4
    send_email(t_data, company)
    print("\nEmail Sent!!")

    return  # end main


# call main()
if __name__ == '__main__':
    main()
