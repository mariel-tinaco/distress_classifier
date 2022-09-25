

import json
from pathlib import Path
import pandas as pd
import sys, os
import pypeln as pl
import asyncio
import functools

from tqdm.asyncio import trange, tqdm
from tqdm import tqdm

from src.datasetloader import DataProcessor, audiosetLoader, extract_media, media_generator, media_extractor
from src.downloader import fetch_m4a_audio
from src.utils.downloader import fullpipe


def get_by_multiple_keywords (keywords : list, source_path):

    processor = DataProcessor()

    filter_keywords = keywords
    dataset_path = source_path

    with open (Path("io/metadata/mapping.json"), 'r') as jsonfile:
        mapping = json.load(jsonfile)
        reversed_mapping = {v:k for k, v in mapping.items()}

    filter_keys = [reversed_mapping[kw] for kw in filter_keywords]


    with open (dataset_path, "r") as file:
        data = processor.load(file, audiosetLoader)

        '''
        Solution for filtering found here https://pandas.pydata.org/docs/reference/api/pandas.Series.str.contains.html
        '''        
        
        filtered_data_list = [data.loc[data['positive_labels'].str.contains(filter_key, regex=False)] for filter_key in filter_keys]

        reducer = lambda x, y: pd.merge(x, y, how='inner', on=['YTID', 'start_seconds', 'end_seconds', 'positive_labels'])

        filtered_data = functools.reduce(reducer, filtered_data_list)

        generator = media_extractor(filtered_data)

        stage = pl.sync.each (fullpipe, generator, workers=10)
        pl.sync.run(stage)


def get_by_keyword (keyword):

    processor = DataProcessor()
    balanced_dataset_path = Path("io/metadata/balanced_train_segments.csv")

    filter_keyword = keyword

    with open (Path("io/metadata/mapping.json"), 'r') as jsonfile:
        mapping = json.load(jsonfile)
        reversed_mapping = {v:k for k, v in mapping.items()}

    filter_key = reversed_mapping[filter_keyword]

    with open (balanced_dataset_path, "r") as file:
        data = processor.load(file, audiosetLoader)

        '''
        Solution for filtering found here https://pandas.pydata.org/docs/reference/api/pandas.Series.str.contains.html
        '''        
        filtered_data = data.loc[data['positive_labels'].str.contains(filter_key, regex=False)]

        generator = media_extractor(filtered_data)

        stage = pl.sync.each (fullpipe, generator, workers=10)
        pl.sync.run(stage)



if __name__ == "__main__":

    get_by_multiple_keywords (['Horse', 'Cough'], source_path=Path("io/metadata/unbalanced_train_segments.csv"))

    # get_by_keyword("Horse")