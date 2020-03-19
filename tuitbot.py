import tweepy
import tkinter
import praw
import requests
import os
import json
import time
#Loging into twitter account

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

try:
    api.verify_credentials()
    print("Twitter authentication OK")
except:
    print("Error during Twitter authentication")

#Logging into reddit account

reddit = praw.Reddit(client_id='',
                     client_secret='',
                     password='',
                     user_agent='',
                     username='')

print(reddit.user.me())


#Delay between posts in minutes
delay = 30
#Scrape top post from front page
while True:
	t = time.localtime()
	print('Starting bot at:' + time.strftime("%H:%M:%S", t))
	print('Scrapping top reddit post')
	with open('json/submitted.json') as jsonFile:
		alreadyUploaded = json.load(jsonFile)
	hotFrontpage = reddit.front.hot(limit=50)
	submission = next(hotFrontpage)

	while submission.name in alreadyUploaded:
		submission = next(hotFrontpage)
	submissionTitle = submission.title
	submissionUrl = submission.url
	alreadyUploaded.append(submission.name)

	with open('json/submitted.json', 'w') as jsonFile:
		json.dump(alreadyUploaded, jsonFile)
	print(submissionTitle)


	#Tweet post on twitter account


	text = submissionTitle + ' #memes #funny'
	mediaUrl = submissionUrl

	filename = 'temp.png'
	request = requests.get(mediaUrl, stream=True)
	if request.status_code == 200:
		with open(filename, 'wb') as image:
			for chunk in request:
				image.write(chunk)

		media = api.media_upload(filename)
		print(media)
		media_ids = []
		media_ids.append(media.media_id)
		api.update_status(media_ids = media_ids, status=text)
		os.remove(filename)
		print("Post uploaded succesfuly")
	else:
		print("Unable to download image")

	t = time.localtime()
	print('Starting bot at:' + time.strftime("%H:%M:%S", t))
	print('Next post in ' + str(delay) + ' minutes')
	time.sleep(60*delay)
