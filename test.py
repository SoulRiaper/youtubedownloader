from pytube import YouTube

video = YouTube("https://youtu.be/VKio7bKURlc?si=l6oqEd6B4Sk8xCob")

video.streams.get_audio_only().download("video.mp4", filename=f"{video.title.replace(' ', '_')}.mp3")
