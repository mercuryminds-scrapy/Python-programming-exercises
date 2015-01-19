import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream

 
# Consumer keys and access tokens, used for OAuth
consumer_key = 'MExVvZT0Q35926Crko5wFrGdr'
consumer_secret = 'YaK4JJ3w4xEHzE0DvOrQRuPsQjquIA5kqLB6i8McVkkRmaof53'
access_token = '2874668814-M5Vh0eC2u9Tmjk4GkO814bGksAQ57AgZ3pdXsB3'
access_token_secret = 'ean5rZki9KAwE3L5alxauTSMTyUFQYwG8enzSGNEKPxmm'
 
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)
user=api.get_user('mercuryminds')
#user = api.me()


# Sample method, used to update a status
#api.update_status('Feeling Happy')


print('Name: ' + user.name)
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


#To get all tweets

for status in tweepy.Cursor(api.user_timeline, id="mercuryminds").items():
    print status.text







class StdOutListener(StreamListener):
    ''' Handles data received from the stream. '''
    def on_data(self, raw_data):
        print raw_data
        return True



    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True # To continue listening

if __name__ == '__main__':

   listener = StdOutListener()

   stream = Stream(auth, listener)

   stream.filter(follow=['2874668814'],track=[])
#   stream.filter(track=['python', 'ruby', 'java'])




