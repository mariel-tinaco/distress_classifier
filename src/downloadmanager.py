from abc import ABC, abstractmethod


class MediaDownloadManager (ABC):
    """ Abstract class for managing media downloads 
    """

    @abstractmethod
    def prepare_download(self):
        ...

    @abstractmethod
    def start_download(self):
        ...


class YouTubeDownloadManager(MediaDownloadManager):
    """ Class for managing downloads from youtube
    
    """

    def prepare_download(self):
        return super().prepare_download()

    def start_download(self):
        return super().start_download()
        