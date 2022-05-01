import sys, os
from pathlib import Path
from abc import ABC, abstractmethod, abstractproperty
from typing import Any, List, Union, Protocol
import shutil
import threading

from pytube import YouTube, Stream
from pytube.cli import on_progress
from pydub import AudioSegment
from tqdm import tqdm

sys.path.append(os.path.join(os.getcwd(), "."))

from media import Media



class MediaDownloader (ABC):

    @abstractmethod
    def prepare (self, url_extension : str):
        """
        Updates video metadata from Video object        
        """

    @abstractmethod
    def run (self, url_extension : str, output_dir : str, file_extension: str):
        """
        Starts Media Download
        """

class YoutubeAudioDownloader (MediaDownloader):

    title = None
    yt = None
    url = None
    pbar = None

    def __init__ (self, file_ext : str):
        self.file_ext = file_ext

    def progress_callback(self, stream: Stream, data_chunk: bytes, bytes_remaining: int) -> None:
        self.pbar.update(len(data_chunk))

    def prepare (self, url_extension : str):
        self.url = f"http://www.youtube.com/watch?v={url_extension}"
        # self.yt = YouTube(self.url, on_progress_callback=self.progress_callback)
        self.yt = YouTube(self.url)
        self.title = self.yt.title

    def run (self, output_dir : str):
        try:
            stream = self.yt.streams.get_audio_only()
            # self.pbar = tqdm(total=stream.filesize, unit="bytes")
            stream.download(output_path=output_dir, filename=Path("{}.{}".format(self.yt.title, self.file_ext)))
            # self.pbar.close()

            return self.yt

        except Exception as e:
            raise e

def trim_audio (path : str, start : float, end : float, output_file_format : str):
    """
    Trim audio, from source path and saves it to the same path. 
    
    :param path: Source path
    :type str:
    :param start: Trim starting point
    :type float:
    :param end: Trim ending point
    :type float:
    :param output_file_format:
    :type str:
    """
    
    # Get the file format of the source file
    file_format = path.split(".")[-1] 

    sound = AudioSegment.from_file(path, format=file_format)
    
    extract = sound[start*1000:end*1000]
    extract.export("{} (trimmed).wav".format(path.split(".")[0]), format=output_file_format)


def download_audio(url_extension, file_ext : str, output_dir : Union[str, Path]) -> MediaDownloader:
    """
    Downloads audio from YouTube URL ID and saves to Output directory. \
        Returns created Media downloader object that contains video metadata

    :param url_extension: ID found at the trail of video URL. \
    :type str: Represented by X's Ex. http://www.youtube.com/watch?v=XXXXXXXXX
    :param file_ext: Preferred Audio file extension
    :type str: "m4a"(Preferred), "mp3", "aac"
    :param output_dir: Download directory
    :type Union[Path, str]:  Path object or string
    """

    downloader = YoutubeAudioDownloader(file_ext=file_ext)
    downloader.prepare(url_extension = url_extension)
    downloader.run(output_dir = output_dir)

    return downloader

def move_audio(filename, src_path : Union[Path, str], paths : List[Union[Path, str]]):
    """
    """
    for path in paths:
        source = Path(f"./{src_path}/{filename}")
        destination = Path(f"./{path}/{filename}")

        thread = threading.Thread(target=shutil.copy2, args=(source, destination))
        thread.start()

def fetch_m4a_audio(media : Media):
    file_ext = "m4a"
    temp_dir = "temp"

    dl = download_audio(media.url_extension, file_ext, temp_dir)
    dl_path = f"{temp_dir}/{dl.title}.{file_ext}"
    trim_audio(dl_path, media.start, media.stop, "wav")

    audio_path = "io/media/audio/"
    move_paths = []

    for tag in media.tags:
        label_path = Path(f"{audio_path}/{tag}/")
        move_paths.append(label_path)
        if tag not in os.listdir(audio_path):
            os.mkdir(label_path)
    
    move_audio(f"{dl.title} (trimmed).wav", f"{temp_dir}/", move_paths)

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

    x1 = threading.Thread(target=fetch_m4a_audio, args=(media_1, ))
    x2 = threading.Thread(target=fetch_m4a_audio, args=(media_2, ))

    x1.start()
    x2.start()
