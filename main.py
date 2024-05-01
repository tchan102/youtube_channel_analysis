from googleapiclient.discovery import build
import os
import numpy as np
import pandas as pd

def youtube_service():
    api_key = os.getenv('YOUTUBE_API_KEY')
    return build('youtube', 'v3', developerKey=api_key)

def get_channel_videos(youtube, channel_id):
    video_ids = []
    next_page_token = None
    while True:
        res = youtube.search().list(channelId=channel_id, part='id', type='video', maxResults=50, pageToken=next_page_token).execute()
        video_ids += [video['id']['videoId'] for video in res['items']]
        next_page_token = res.get('nextPageToken')
        if not next_page_token:
            break
    return video_ids

def get_video_details(youtube, video_ids):
    video_lengths = []
    for i in range(0, len(video_ids), 50):
        res = youtube.videos().list(id=','.join(video_ids[i:i+50]), part='contentDetails').execute()
        video_lengths += [parse_duration(video['contentDetails']['duration']) for video in res['items']]
    return np.array(video_lengths)

def parse_duration(duration):
    import isodate
    return isodate.parse_duration(duration).total_seconds()

youtube = youtube_service()
channel_id = 'channel_id' 
video_ids = get_channel_videos(youtube, channel_id)
video_lengths = get_video_details(youtube, video_ids)

df = pd.DataFrame({
    'VideoID': video_ids,
    'LengthInSeconds': video_lengths
})
df.to_pickle('video_data.pkl')