import sys, os
from abc import ABC, abstractmethod
from pytube import YouTube

import threading

sys.path.append(os.path.join(os.getcwd(), "."))


class MediaDownload (ABC):

    @abstractmethod
    def start (self):
        ...



def download(yt_object : YouTube):

    dlpath = f"audio/"

    stream = yt_object.streams.get_audio_only()
    stream.download(output_path=dlpath,filename=f"{yt_object.title}.mp3")

if __name__ == "__main__":

    yt1 = YouTube("http://www.youtube.com/watch?v=-0xzrMun0Rs")
    yt2 = YouTube("http://www.youtube.com/watch?v=-0jeONf82dE")

    x1 = threading.Thread(target=download, args=(yt1,))
    x2 = threading.Thread(target=download, args=(yt2,))

    x1.start()
    x2.start()

