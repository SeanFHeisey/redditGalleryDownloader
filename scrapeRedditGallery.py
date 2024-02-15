# Sean Heisey
# reddit gallery downloader
# 2/14/2024

import praw
import requests
import os

# enter credentials
reddit = praw.Reddit(
    client_id='client ID',
    client_secret='client_secret',
    username='reddit username',
    password='reddit password',
    user_agent='app name by name',
)

def getGallery(url, folderNumber):
    submission = reddit.submission(id=url.split('/')[-1])
    galleryData = submission.gallery_data
    outputDirectory = folderNumber
    os.makedirs(outputDirectory, exist_ok=True)
    for i in submission.media_metadata.values():
        if 's' in i and 'u' in i['s']:
            imageUrl = i['s']['u']
            response = requests.get(imageUrl)
            if response.status_code == 200:
                randomOrder = i.get('id', 'N/A')
                newName = 0
                for j, k in enumerate(galleryData['items']):
                    redditOrder = k.get('media_id', 'N/A')
                    if redditOrder in randomOrder:
                        newName += j
                imageFilename = os.path.join(outputDirectory, f'{str(newName)}.jpg')
                with open(imageFilename, 'wb') as file:
                    file.write(response.content)
                print(f'{imageFilename}')

def getPosts(numberOfPosts):
    posts = reddit.subreddit(subredditName).hot(limit=None)
    for i, j in enumerate(posts):
        url = j.url
        if 'https://www.reddit.com/gallery/' in url:
            getGallery(url, str(i-1))
            if i>=numberOfPosts-1:
                break
            
print('Which subreddit do you want to download?')
subredditName = input('Enter name: ')
print('How many gallerys would you like to be downloaded?')
galleryAmount = int(input('Enter number: '))  
getPosts(galleryAmount)
print('Done!')
