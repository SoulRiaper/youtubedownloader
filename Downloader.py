from pytube import YouTube

video_url = "https://www.youtube.com/watch?v=81kxfF08bOA"

video = YouTube(video_url)

# for i, stream in enumerate(video.streams.get_audio_only()):
#     print(f"{i}: {stream}")
title = video.title
video = video.streams.get_audio_only()
video.download("./video.mp4", filename=f"{title}.mp3")



