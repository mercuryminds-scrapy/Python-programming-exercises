import tweepy
import time
from datetime import datetime
import psycopg2


"""Un comment the below modules to get the real time tweets"""
# from tweepy.streaming import StreamListener
# from tweepy import Stream



# Consumer keys and access tokens, used for OAuth
consumer_key = 'oM6OieC09OJJLeVJ8UbZkJPJO'
consumer_secret = 'z0YUK4NNpOoSSRhY9dJqjVLzPhhU0V38OvN7ELvurdhnfLZi8D'
access_token = '2989212755-8KfCUDwcs8tdO27wme3qXCTnUnbBGooi85vdZoE'
access_token_secret = 'AOAboTWRsOqAyfyIVIqQEWZicT7MkCMxhueSy600meu2M'


# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


""" Database Creation"""
con = psycopg2.connect(database="mm", user="postgres", password="mercuryminds", host="localhost")
cur = con.cursor()



"""Getting tweets from user timeline"""

def tweet(twitter_profile, business_id, last_tweet_time):

    """Open file to save the data locally"""
    fn = '%s' % twitter_profile+'_tweets.csv'
    f = open(fn, 'w')
    f.write('Business_ID\tName\tTime\tTweets\tRetweet_Count\tFav_count\n')

    tw = tweepy.Cursor(api.user_timeline, id=twitter_profile).items()
    while True:
        try:
            c = tw.next()
            user = c.user.name.encode('utf-8')
            tm = c.created_at

            data = c.text.encode('utf-8').replace("'", "").replace('\n', '').replace('"', '')
            fc = c.favorite_count
            rt = c.retweet_count
            # try:
            #     old_tweet_time = datetime.strptime(last_tweet_time, '%Y-%m-%d %H:%M:%S')
            # except:
            #     old_tweet_time = datetime.strptime('1', '%d')
            if tm > last_tweet_time:
                print business_id, user, tm, data, fc, rt

                """Insert the tweet details into the csv file"""
                
                f.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (business_id, user, tm, data, fc, rt))

                """Insert data into DB"""

                sql=("insert into public.mmtweet(id, username, time, tweet, r, f)  values('%s','%s','%s','%s','%s','%s')"%(business_id, user, tm, data, fc, rt))
                cur.execute(sql)
                con.commit()

            else:
                break

        except tweepy.TweepError:
            print "Got Exception Please wait for 15 Min to ReConnect"
            time.sleep(60 * 15)
            continue
        except StopIteration:
            break





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


"""Checkdb function is to check the data into our DB"""

def checkdb(tname):

    """Get the Unique user name from the DB"""
    sql = ("select distinct username from public.mmtweet")
    cur.execute(sql)
    rows = cur.fetchall()

    de=[]
    for r in rows:
        de.append(r[0])
#    """ de list has list of user names in our DB """

    for i in range(len(de)):
        if de[i].lower() == tname.lower():
            print "Previoius Data Found for the given Twitter Profile name"
            cur.execute("select distinct id from public.mmtweet where username='%s'"%de[i])
            r=cur.fetchall()
            b_id= r[0][0]
            cur.execute("select max(time) from public.mmtweet")
            r=cur.fetchall()
            ti=r[0][0]
            """Get the business_id and max(time) !"""
            print b_id, ti
            """Call the tweet function with username and  business_id and time from the DB"""
            tweet(twitter_profile_name, b_id, ti)

        else:
            """No Previous Data in DB so Take all tweets"""
            alltweets()
    """Below If works if the DB is empty"""
    if len(de)==0: alltweets()


"""Get all tweets by calling alltweet function"""

def alltweets():
    print "No previous data for given profile\n"
    b_id=input("Enter Business Id")
    ti = datetime.strptime('1', '%d')
    tweet(twitter_profile_name,b_id,ti)


"""Enter the twitter Profile """
twitter_profile_name='RKANANDHAKUMAR'

checkdb(twitter_profile_name)

"""DB connection close"""
con.close()