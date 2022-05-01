import sys, os
from abc import ABC, abstractmethod, abstractproperty
from pytube import YouTube
from pydub import AudioSegment
from pathlib import Path
from typing import Any, Union, Protocol

import threading

sys.path.append(os.path.join(os.getcwd(), "."))

from media import Media

class MediaDownloader (ABC):

    @abstractmethod
    def run (self, url_extension : str, output_dir : str, file_extension: str):
        ...

class YoutubeAudioDownloader (MediaDownloader):

    def run (self, url_extension : str, output_dir : str, file_extension: str):
        url = f"http://www.youtube.com/watch?v={url_extension}"
        try:
            yt = YouTube(url)

            stream = yt.streams.get_audio_only()
            title = yt.title
            stream.download(output_path=output_dir, filename=Path("{}.{}".format(title.replace(" ", "_"), file_extension)))

            return yt

        except Exception as e:
            raise e

def trim_audio (clip_path, start, end):

    sound = AudioSegment.from_file(clip_path, format="m4a")
    extract = sound[start*1000:end*1000]

    extract.export("{}_clipped.wav".format(clip_path.split(".")[0]), format="wav")

def fetch_audio(media : Media, file_ext : str):

    audio_dir = Path("./io/media/audio/{}".format(media.tags[0]))

    downloader = YoutubeAudioDownloader()
    media_obj = downloader.run(
        url_extension = media.url_extension,
        output_dir = audio_dir,
        file_extension= file_ext )

    full_dir = f"{audio_dir}/{media_obj.title}.{file_ext}"

    trim_audio(full_dir.replace(" ", "_"), media.start, media.stop)


if __name__ == "__main__":

    media_1 = Media (
        url_extension="-1PZQg5Gi8A",
        start= 30.000,
        stop=40.000,
        tags=["Smash"])

    media_2 = Media (
        url_extension="-2EKWgTNEYU",
        start=30.000,
        stop=40.000,
        tags=["Radio"]
    )

    x1 = threading.Thread(target=fetch_audio, args=(media_1, "m4a"))
    x2 = threading.Thread(target=fetch_audio, args=(media_2, "m4a"))

    x1.start()
    x2.start()

