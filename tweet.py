import tweepy
import time

"""Un comment the below modules to get the real time tweets"""

# from tweepy.streaming import StreamListener
# from tweepy import Stream

"""Un comment while passing the tweets to Mysql DB"""
# import MySQLdb


# Consumer keys and access tokens, used for OAuth
consumer_key = 'oM6OieC09OJJLeVJ8UbZkJPJO'
consumer_secret = 'z0YUK4NNpOoSSRhY9dJqjVLzPhhU0V38OvN7ELvurdhnfLZi8D'
access_token = '2989212755-8KfCUDwcs8tdO27wme3qXCTnUnbBGooi85vdZoE'
access_token_secret = 'AOAboTWRsOqAyfyIVIqQEWZicT7MkCMxhueSy600meu2M'


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
def tweet(twitter_profile):
    fn='%s'%twitter_profile+'_tweets.csv'
    f=open(fn,'w')
    f.write('Name\tTime\tTweet\n')

    tw=tweepy.Cursor(api.user_timeline, id=twitter_profile).items()
    while True:
        try:
            c= tw.next()
            try:
                a= c.retweeted_status.user.name
            except:
                a= c.user.name
            b= c.created_at
            d= c.text.encode('ascii','ignore').replace("'","").replace('\n','').replace('"','')

            """Insert the tweet details into the csv file"""
            f.write('%s\t%s\t%s\n'%(a,b,d))

            """Create a tabel called tweet with 3 columns and insert the data by uncomment"""
            #sql=("insert into tweet(title,time,tweet) values('%s','%s','%s')"%(a,b,d))
            #cur.execute(sql)
            #con.commit()


        except tweepy.TweepError:
            print "Got Exception"
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




"""Pass the twitter profile name to get the whole tweets"""


tweet('foodsafeguru')