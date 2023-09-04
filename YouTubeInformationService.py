from googleapiclient.discovery import build
from os import getenv
import re


class YouTubeInfo:
    def __init__(self, api_key):
        self.youtube = build("youtube", "v3", developerKey=api_key)

    def get_playlist_ids(self, playlist_url: str):
        playlist_id = re.findall(r'(?<=list=)[^&#]+', playlist_url)[0]
        req = self.youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50
        )
        res = req.execute()
        video_urls = []

        for item in res['items']:
            video_id = item["contentDetails"]["videoId"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_urls.append(video_url)

        return video_urls
