from pytube import YouTube
from io import BytesIO
from ProjectExceptions import TooBigFileException


class AudioDownloader:
    def __init__(self):
        self.audio: YouTube

    def download(self, url: str):
        self.audio = YouTube(url)
        if self.audio.streams.get_audio_only().filesize > 45 * 1024 * 1024:
            raise TooBigFileException
        buff = BytesIO()
        self.audio.streams.get_audio_only().stream_to_buffer(buff)
        buff.seek(0)
        return buff
