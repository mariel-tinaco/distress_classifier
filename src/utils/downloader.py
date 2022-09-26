import abc
from pathlib import Path
from token import EXACT_TOKEN_TYPES
from typing import Callable
import numpy as np
from pytube import YouTube, Stream
from pytube.exceptions import VideoPrivate
from dataclasses import dataclass
import sys, os
from pydub import AudioSegment

sys.path.append(os.path.join(os.getcwd(), '.'))

from src.media import Media

TEMP_DIR = Path.cwd() / 'temp'

@dataclass
class AudioSample:
    data : np.ndarray
    sr : int

    @property
    def duration(self):
        return 1/self.sr


def fullpipe (media : Media):
    audio_path = Path.cwd() / 'io' / 'media' / 'audio'

    filename = yt_audio_downloader(media.url_extension)

    if filename:
        sound_file = AudioSegment.from_file(TEMP_DIR / filename, 'm4a')
        
        # Trim

        trimmed_audio = sound_file[media.start*1000: media.stop*1000]

        #Convert and move

        wavfilename = filename.split('.')[0] + '.wav'

        for tag in media.tags:
            label_path = audio_path / tag
            if tag not in os.listdir(audio_path):
                os.mkdir(label_path)

            wavfullfilepath = label_path / wavfilename

            if wavfullfilepath not in os.listdir(label_path):
                trimmed_audio.export(wavfullfilepath, 'wav')
        
        os.remove(TEMP_DIR / filename)

def yt_audio_downloader (yt_url_extension : str) -> np.ndarray:

    file_ext = 'm4a'

    try:
        yt = YouTube(f"http://www.youtube.com/watch?v={yt_url_extension}")
        fn = "{}.{}".format(
            yt.title.replace(' ', '_') \
                .replace('/', '_') \
                .replace('(', '') \
                .replace(')','') \
                .replace('-','_'), 
            file_ext)
        stream = yt.streams.get_audio_only()
        # stream.download(output_path=TEMP_DIR, filename=fn)
        stream.download(output_path=TEMP_DIR, filename=fn)

        return fn

    except VideoPrivate:
        print(f"Unable to download private video: {yt_url_extension}")

    except TypeError:
        print(f"Type error")

    except Exception as e:
        print (e)

    return


if __name__ == "__main__":

    media_2 = Media (
        url_extension="-2EKWgTNEYU",
        start=30.000,
        stop=40.000,
        tags=["Radio"]
    )
    fullpipe(media_2)
