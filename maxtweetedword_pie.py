import tweepy
import os
from collections import Counter
from matplotlib import pyplot as plt

#add Twitter API keys here
consumer_key = '' 
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

words_list = []
words_to_filter = []

filtering = open('words_to_filter.txt')
for line in filtering:
    words_to_filter = line.split()

all_tweets = []
user = input("enter user: ")
statuses_count = api.get_user(screen_name = user).statuses_count
print(statuses_count)

target_timeline = api.user_timeline(screen_name = user, count = 200)
all_tweets.extend(target_timeline)
oldest_id = all_tweets[-1].id - 1

while len(target_timeline) > 0:
    target_timeline = api.user_timeline(screen_name = user, count = 50, max_id = oldest_id,)
    all_tweets.extend(target_timeline)
    oldest_id = all_tweets[-1].id - 1


target_timeline =  api.user_timeline(screen_name = user, count = len(all_tweets) - statuses_count)
all_tweets.extend(target_timeline)

print(len(all_tweets))

for tweet in all_tweets:
    content = (tweet.text).split()
    for word in content:
        word = word.lower() #case insensitive 
        if word.isalnum(): #isalnum() gets rid of emojis and other non alphanumeric characters 
            if word not in words_to_filter:
                if word[0] != '@' or word[0:5] == 'https': #this filters quote tweets and replies to a particular account
                    words_list.append(word)
            else:
                continue

#COUNTING
number_of_results = int(input("how many of your top words do you want to see? "))
most = Counter(words_list).most_common(number_of_results) #this counts the number of occurences of a word and finds top number_of_results words

#creating two lists as data sources for the pie chart
words = list()
count = list()
for item in most:
    words.append(item[0])
    count.append(item[1])

plt.pie(count, labels=words, autopct="%1.1f%%") #making the pie chart
plt.title(user + "'s top " + number_of_results +" tweeted words")
plt.savefig('fig.jpg') #saving the chart as a .jpg file
plt.show()
media = api.media_upload('fig.jpg') # we need to upload the image first, before tweeting
tweet = '@' + user + " 's twitter pie"
api.update_status(status = tweet, media_ids = [media.media_id]) # sending the tweet out
os.remove('fig.jpg') # deleting the file so we don't unnecessarily use up our storage, and also don't store information
