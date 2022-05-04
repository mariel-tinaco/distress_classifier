from pathlib import Path
from io import TextIOWrapper
import pandas
from csv import reader
import json
from typing import Callable

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


if __name__ == "__main__":
    loader = DataProcessor()
    path = "io/metadata/balanced_train_segments.csv"

    with open(Path(path), "r") as file:
        data = loader.load(file, audiosetLoader)

    print(data)