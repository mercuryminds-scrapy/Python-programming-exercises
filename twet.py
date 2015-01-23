import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
import MySQLdb
import time
 
# Consumer keys and access tokens, used for OAuth

consumer_key = 'oM6OieC09OJJLeVJ8UbZkJPJO'
consumer_secret = 'z0YUK4NNpOoSSRhY9dJqjVLzPhhU0V38OvN7ELvurdhnfLZi8D'
access_token = '2989212755-8KfCUDwcs8tdO27wme3qXCTnUnbBGooi85vdZoE'
access_token_secret = 'AOAboTWRsOqAyfyIVIqQEWZicT7MkCMxhueSy600meu2M'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Database Creation
con=MySQLdb.connect('localhost','root','root','mysql')
cur=con.cursor()

 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)
user=api.get_user('TSmoothieCafe')
print user
#user = api.me()


# Sample method, used to update a status
#api.update_status('Feeling Happy')


print('Name: ' + user.name)
print user.statuses_count
print user.created_at
print user.default_profile
print user.default_profile_image
print user.description
print user.entities
print user.id
print user.followers_count
print('Friends: ' + str(user.friends_count))
print user.status
print user.statuses_count
print user.url



# page_list=[]
#
# for page in tweepy.Cursor(api.user_timeline, include_rts=True,count=200).pages(''):
#     page_list.append(page)
#
#
# for page in page_list:
#     for status in page:
#        print status.text


