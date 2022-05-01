import sys, os
from abc import ABC, abstractmethod, abstractproperty
from pytube import YouTube
from pathlib import Path
from typing import Any, Union, Protocol

import threading

sys.path.append(os.path.join(os.getcwd(), "."))

from media import Media

class YoutubeMediaDownloader (ABC):

    @abstractmethod
    def run (self, url_extension : str, output_dir : str, file_extension: str):
        ...

class YoutubeAudioDownloader (YoutubeMediaDownloader):

    def run (self, url_extension : str, output_dir : str, file_extension: str):
        url = f"http://www.youtube.com/watch?v={url_extension}"
        try:
            yt = YouTube(url)

            stream = yt.streams.get_audio_only()
            stream.download(output_path=output_dir, filename=Path(f"{yt.title}.{file_extension}"))

        except Exception as e:
            raise e


def fetch_audio(media : Media, file_ext : str):

    downloader = YoutubeAudioDownloader()
    downloader.run(
        url_extension = media.url_extension,  
        output_dir = Path("io/media/audio/{}".format(media.tags[0])),
        file_extension= file_ext )

if __name__ == "__main__":

    media_1 = Media (
        url_extension="-1PZQg5Gi8A",
        start= 30.000, 
        stop=40.000,
        tags=["Smash, crash"])

    media_2 = Media (
        url_extension="-2EKWgTNEYU",
        start=30.000,
        stop=40.000,
        tags=["Radio"]
    )

    x1 = threading.Thread(target=fetch_audio, args=(media_1, ".mp3"))
    x2 = threading.Thread(target=fetch_audio, args=(media_2, ".mp3"))

    x1.start()
    x2.start()

