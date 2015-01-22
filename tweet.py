import tweepy
import time
from datetime import datetime

"""Un comment the below modules to get the real time tweets"""

# from tweepy.streaming import StreamListener
# from tweepy import Stream

"""Un comment while passing the tweets to Mysql DB"""
# import MySQLdb


# Consumer keys and access tokens, used for OAuth
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''


# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

""" Database Creation"""
# con=MySQLdb.connect('localhost','root','root','mysql')
# cur=con.cursor()
# Creation of the actual interface, using authentication
api = tweepy.API(auth)
"""To get all tweets from user timeline"""
"""Pass twitter profile name as keword to tweet function"""


def tweet(twitter_profile, business_id, x):
    fn = '%s' % twitter_profile+'_tweets.csv'
    f = open(fn, 'w')
    f.write('Business_ID\tName\tTime\tTweets\tRetweet_Count\tFav_count\n')

    tw = tweepy.Cursor(api.user_timeline, id=twitter_profile).items()
    while True:
        try:
            c = tw.next()
            try:
                a = c.retweeted_status.user.name.encode('utf-8')
            except:
                a = c.user.name.encode('utf-8')
            b = c.created_at

            d = c.text.encode('utf-8').replace("'", "").replace('\n', '').replace('"', '')
            fc = c.favorite_count
            rt = c.retweet_count
            try:
                old_tweet_time = datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
            except:
                old_tweet_time = datetime.strptime('1', '%d')
            if b > old_tweet_time:
                print business_id, a, b, d, fc, rt
                """Insert the tweet details into the csv file"""
                f.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (business_id, a, b, d, fc, rt))
                """Create a tabel called tweet with 3 columns and insert the data by uncomment"""
            else:
                break
            # sql=("insert into tweet(title,time,tweet) values('%s','%s','%s')"%(a,b,d))
            # cur.execute(sql)
            # con.commit()
        except tweepy.TweepError:
            print "Got Exception Please wait for 15 Min to ReConnect"
            time.sleep(60 * 15)
            continue
        except StopIteration:
            break


# con.commit()
# cur.close()
# con.close()
#
"""Un comment the below class to get the real time tweets"""
# class StdOutListener(StreamListener):
#     ''' Handles data received from the stream. '''
#     def on_data(self, raw_data):
#         print raw_data
#         return True
#
#
#
#     def on_error(self, status_code):
#         print('Got an error with status code: ' + str(status_code))
#         return True # To continue listening
#
# if __name__ == '__main__':
#
#    listener = StdOutListener()
#
#    stream = Stream(auth, listener)
"""Use the twitter Id to follow the realtime tweets follow=[' Id here']"""
#   stream.filter(follow=['2874668814'],track=[])
"""Pass the twitter profile name,Business_ID and last tweet time to get the whole tweets"""

"""For Example ***tweet('firebrewbar',10004,'2015-01-20 01:25:51')  to get all tweets give empty string to tweet time(last arg)***"""

tweet('firebrewbar', 10006, '2015-01-20 01:25:51')
