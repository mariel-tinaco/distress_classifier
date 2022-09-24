import json
from pathlib import Path
from io import TextIOWrapper
import threading
import pandas
from csv import reader
from typing import Callable
import tqdm

from src.downloader import fetch_m4a_audio
from src.media import Media
from src.ontology import extract_audioset

def audiosetLoader(file : TextIOWrapper) -> pandas.DataFrame:
    """
    Data Loader based on the format of training segments from Audioset
    https://research.google.com/audioset/download.html
    
    :param file: CSV file wrapper
    :type TextIOWrapper:

    :return Pandas DataFrame:
    """
    csv_reader = reader(file)

    header = next(csv_reader)
    header = next(csv_reader)
    header = next(csv_reader)
    header[0] = header[0].replace("#", "")
    header = [col.replace(" ", "") for col in header]
    
    Data = {i : [] for i in header}

    for row in csv_reader:
        store = []
        for i, col in enumerate(row):
            if i < 3:
                Data[header[i]].append(col)
            else:
                store.append(col.replace('"', '').replace(" ", ""))
        Data[header[3]].append(store)
    
    data = pandas.DataFrame(Data)

    return data



class DataProcessor:
    
    def load(self, filewrapper : TextIOWrapper, loader : Callable) -> pandas.DataFrame:
        """
        Generic data loader extracted within context manager

        :param filewrapper: 
        :type TextIOWrapper:
        :param loader:
        :type Callable:
        """
        
        return loader(filewrapper)


def extract_media(dataframe : pandas.DataFrame):

    audioset = extract_audioset(file=Path("ontology/ontology.json"), key=1)

    with open("io/metadata/mapping.json", "r") as read:
        mapping = json.load(read)

    count = 0

    media_list = []

    for index, row in dataframe.iterrows():

        labels = [mapping[i] for i in row["positive_labels"]]

        if "Screaming" in labels:
            media = Media(
                url_extension= row["YTID"],
                start= row["start_seconds"],
                stop= row["end_seconds"],
                tags=labels)

            media_list.append(media)

        count += 1

    return media_list


def media_generator (dataframe : pandas.DataFrame):

    with open("io/metadata/mapping.json", "r") as read:
        mapping = json.load(read)

    for index, row in dataframe.iterrows():

        labels = [mapping[i] for i in row['positive_labels']]

        yield Media (
            url_extension= row['YTID'],
            start= row["start_seconds"],
            stop = row["end_seconds"],
            tags=labels
        )
    

def media_extractor (dataframe : pandas.DataFrame):

    with open("io/metadata/mapping.json", "r") as read:
        mapping = json.load(read)

    container = []

    for index, row in dataframe.iterrows():

        labels = [mapping[i] for i in row['positive_labels']]

        container.append(
            Media (
                url_extension= row['YTID'],
                start= eval(row["start_seconds"]),
                stop = eval(row["end_seconds"]),
                tags=labels
            )
        )

    return container

if __name__ == "__main__":
    loader = DataProcessor()
    path = "io/metadata/balanced_train_segments.csv"

    with open(Path(path), "r") as file:
        data = loader.load(file, audiosetLoader)

    media_list = extract_media(data)

    for media in media_list:
        x = threading.Thread(target=fetch_m4a_audio, args=(media, ))    
        x.start()