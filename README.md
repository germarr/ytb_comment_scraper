# Get all the Comments from a Youtube Video

This script is part of my research project called "What Topics Drives Youtube MX?". You can check the whole project [**here**](https://gmarr.com/).

This Python script will get all the comments from a Yotube (trough the Youtube API) and export them to a CSV file. 

Here's an example of the final result you can get after running the script:

## **Index**
---
* Read the Requirements for this project [**here**](#requirements)
* I want to learn how the code works! 😮--> Click [**here**](#full-tutorial) for the full tutorial.
* Just give me a quick summary 😎 --> Click [**here**](#quick-tutorial)

## **Requirements**
---
To run this script I would recommend to have some understanding of the next technologies:
* Python
    * `for` loops
    * functions
    * pip. 
        * [Here](https://realpython.com/what-is-pip/) you can find a really good article that expalins what is pip.
    * pandas. 
        * [This](https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html) is a gentle introduction to the pandas library.
* JSON
    * The general structure of a JSON file
* API's
    * Specifically, the tutorial is going to make more sense if you know what is an API Key. To learn more about API's I recommend to watch this [video](https://www.youtube.com/watch?v=GZvSYJDk-us&t=4641s). The video shows the inner workings of the [Trello API](https://developer.atlassian.com/cloud/trello/rest/) however, the concepts that are shown can be applied to any API. This is my "go-to" reference guide when I'm stucked.

In addition to the concepts mentioned above, before you start the tutorial be sure to have:

* A Youtube API Key
    * In order to retrieve the data from Youtube we're going to use the [Youtube API](https://developers.google.com/youtube/v3). All the API's from Google properties require a Google Account and autorization credentials.
    * To learn how to setup a Google Account and get this credentials you can follow this [tutorial](https://developers.google.com/youtube/registering_an_application).
    * Once you have your credentials, you need to request an API Key. You can follow [this instructions](https://cloud.google.com/resource-manager/docs/creating-managing-projects?visit_id=637472330160631271-1024614839&rd=1) to get your API Key.
    * If you want additional information about the API setup, Youtube offers a nice introduction [here](https://developers.google.com/youtube/v3/getting-started).
* A Code Editor
    * I use VS Code. You can download it [here](https://code.visualstudio.com/).
* Python
    * If you use a Mac you already have Python installed. If you use a Windows PC or Linux, you can download Python [here]("").
    * The `pandas` library. You can download it from [here](https://pandas.pydata.org/).

## **Full Tutorial**
---

1. Download the [google python client](https://github.com/googleapis/google-api-python-client) via pip. 

```python
pip install google-api-python-client
```
2. Import the “build” function from the Google Python Client. This function helps to abstract a lot of the code needed to use the Youtube API.

```python
from googleapiclient.discovery import build
```
3. Get your API Key from the [Google Developer Console](https://console.developers.google.com/) and copy it. 
4. Create a variable called `api_key` and paste the API Key that you copied from the Google Developer Console. Then create a variable called `youtube` and assign it the `build()` function with the parameters
 `youtube`, `v3` and `developerKey = api_key`. Finally, create a variable called `url` and paste the url of the video you want to get the comments from. 

```python
api_key= "<Paste your API KEY here>"

youtube = build("youtube","v3", developerKey=api_key)

url="https://youtube.com/..."
```

* [Here](https://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.discovery-module.html#build) you can learn all the arguments that can be used in the `build()` function.
* I would also recommend checking all the different methods that the youtube API can use. You can find them [here](https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.html).

5. Before we continue, it's important to understand the `videos()` method inside the `build()` function that we created. [Here]("https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.videos.html") you can find all the methods that can be used on `video()`. For this tutorial we’re going to use the `list()` method. [Here]("https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.videos.html#list") are all the parameters that can be used inside `list()`. 


6. In addition to the `videos()` method we need to understand the `commentThread()` method and the `list()` method that applies to it. [Here](https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.commentThreads.html) you can find the documentation.

7. Using the `videos().list()` method we're going to request the key information and stats for the video you selected.
```python
    # Get the ID of the video by splitting the URL
    single_video_id = url.split("=")[1].split("&")[0]

    # Use the list() method to extract a JSON with key information from the video including the name of the video and the channelID.  We're going to use this data later.
    video_list=youtube.videos().list(part="snippet",id=single_video_id).execute()
    channel_id= video_list["items"][0]["snippet"]["channelId"]
    title_single_video= video_list["items"][0]["snippet"]["title"]

    # We are going to declare 3 variables "playlist_id", "forUserName" and "nextPageToken". This variables will store data that we're going to create once we ran the whole script.
    playlist_id = None
    forUserName = None
    nextPageToken_comments = None

    # We declare an empty list. This list will be converted into a csv at the end of our script.
    commentsone=[]
```
8. We're going to create a `while` loop that will keep making calls to the youtube API until we get all the comments from the youtube video. Every response is a JSON file that we will store in a variable called `pl_response_comment` 
* The `commenthThread` method offers a parameter called `pageToken`. This parameter will help us to keep new comments coming from the API call. You can learn more about this parameter [here](https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.commentThreads.html#list).
```python
    while True:
        #Request the first 50 videos of a channel. The result is store in a variable called "pl_response".
        #PageToken at this point is "None"
        pl_request_comment= youtube.commentThreads().list(part=["snippet","replies"],
                                            videoId=single_video_id, 
                                            maxResults=50,
                                            pageToken= nextPageToken_comments)
        pl_response_comment = pl_request_comment.execute()
```
9. Our `pl_response_comment` contains all the information we need. To order everything in a more readable format, we're going to write a `for` loop that will iterate in every element of the variable and `append` the information into the `commentsone` emt that we already created. We're going to repeat this process until the API reached the first comment of the video. We keep control of this using the `pageToken` parameter that I mentioned in the step number 8 of this tutorial.

```python
        ## Send the amount of views and the URL of each video to the videos empty list that was declared at the beginning of the code.
        for i in pl_response_comment["items"]:
            vid_comments = i["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
            comm_author = i["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
            comm_author_id = i["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]["value"]
            comm_date = i["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
            comm_likes = i["snippet"]["topLevelComment"]["snippet"]["likeCount"]
            new_var=i.get("replies","0")

        # Append the results into the empty list "commentsone"
            commentsone.append({
                "comm_date":comm_date,
                "author":comm_author,
                "author_id":comm_author_id,
                "likes":comm_likes,
                "comment":vid_comments,
                "video_id":single_video_id
            })
        
            if new_var != "0":
                replies_commentsone.append({
                    "replies":new_var
                })
        nextPageToken_comments = pl_response_comment.get("nextPageToken")

        # The for loop will break once the response from "pageToken" reaches the first page of the comments.
        if not nextPageToken_comments:
            break
```
10. The final step is to turn the `commentsone` list into a CSV file. This is a 3 step process. First we import the `pandas` library, then we call the `from_dict` on the `commentsone` variable. This will turn the variable into a `pandas dataframe`. Once we have the dataframe we turn it into a CSV file usind the `to_csv` method. We can use the `title_single_video` variable we created to name the file automatically or we can name it whatever we want.
To learn more about this `pandas` methods, click [here](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_dict.html)

```python
import pandas as pd

 pd.DataFrame.from_dict(commentsone).to_csv(f"{title_single_video}.csv")
```

The final version of the code should look similar to this:
```python
import pandas as pd

## Call the "build()" function from the Python-client
from googleapiclient.discovery import build

api_key = input("API KEY: ")
youtube = build("youtube","v3", developerKey=api_key)
url = input("VIDEOURL: ")

single_video_id = url.split("=")[1].split("&")[0]

video_list=youtube.videos().list(part="snippet",id=single_video_id).execute()

channel_id= video_list["items"][0]["snippet"]["channelId"]
title_single_video= video_list["items"][0]["snippet"]["title"]

playlist_id = None
forUserName = None
nextPageToken_comments = None

replies_commentsone=[]
commentsone=[]

while True:
    pl_request_comment= youtube.commentThreads().list(part=["snippet","replies"],
    videoId=single_video_id, 
    maxResults=50,
    pageToken= nextPageToken_comments)
    
    pl_response_comment = pl_request_comment.execute()

    for i in pl_response_comment["items"]:
        vid_comments = i["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
        comm_author = i["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        comm_author_id = i["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]["value"]
        comm_date = i["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
        comm_likes = i["snippet"]["topLevelComment"]["snippet"]["likeCount"]
        new_var=i.get("replies","0")
        
        commentsone.append({
            "comm_date":comm_date,
            "author":comm_author,
            "author_id":comm_author_id,
            "likes":comm_likes,
            "comment":vid_comments,
            "video_id":single_video_id
        })
        
        if new_var != "0":
            replies_commentsone.append({
                "replies":new_var
            })

        nextPageToken_comments = pl_response_comment.get("nextPageToken")

    if not nextPageToken_comments:
        break
    
pd.DataFrame.from_dict(commentsone).to_csv(f"{title_single_video}.csv")
```

## **Quick Tutorial**
---
1. Be sure to read all the [**Requirements**](#requirements) before continuing.
2. Download the [google python client](https://github.com/googleapis/google-api-python-client) via pip. 

```python
pip install google-api-python-client
```

3. Run the `comment_scrapper.py` script. The script will ask for a Google `api_key` and the link of the youtube video from which we want to get all the comments.

```console
python comment_scrapper.py

API KEY: < Paste the Google API Key when prompted >
VIDEOURL: < Paste Youtube Video URL when prompted >
```

4. The script will run and it will store the result, a CSV file, on the same file the pythons script is stored.
```python
pwd

comment_scrapper.py
title_of_the_video.csv
```
5. And that's it! 
Just remember that there's a certain number of API calls that can be made per day. So a video with millions of comments can make you reach that API limit. Each API call returns 50 comments, so a video with 4,000,000 comments can require 80,000 calls.

