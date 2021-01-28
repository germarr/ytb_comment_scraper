import pandas as pd

## Call the "build()" function from the Python-client
from googleapiclient.discovery import build

api_key = input("API KEY: ")
youtube = build("youtube","v3", developerKey=api_key)
url = input("VIDEOURL: ")

def get_comments(url):
    # Get the ID of the video by splitting the URL
    single_video_id = url.split("=")[1].split("&")[0]
    # Use the list() method to extract a JSON with key information 
    # from the video.
    video_list=youtube.videos().list(part="snippet",id=single_video_id).execute()
    channel_id= video_list["items"][0]["snippet"]["channelId"]
    title_single_video= video_list["items"][0]["snippet"]["title"]
    playlist_id = None
    forUserName = None

    nextPageToken_comments = None
    commentsone=[]

    while True:
        #Request the first 50 videos of a channel. This is the full dictionary. The result is store in a variable called "pl_response".
        #PageToken at this point is "None"
        pl_request_comment= youtube.commentThreads().list(part=["snippet","replies"],
                                            videoId=single_video_id, 
                                            maxResults=50,
                                            pageToken= nextPageToken_comments)
        pl_response_comment = pl_request_comment.execute()

        ## Send the amount of views and the URL of each video to the videos empty list that was declared at the beginning of the code.
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
    
    for i in commentsone[:10]:
        print(i["comment"])

    
    pd.DataFrame.from_dict(commentsone).to_csv(f"comments/{title_single_video}.csv")

get_comments(url)
