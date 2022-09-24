

import json
from pathlib import Path
import sys, os
import pypeln as pl
import asyncio
from tqdm.asyncio import trange, tqdm
from tqdm import tqdm

from src.datasetloader import DataProcessor, audiosetLoader, extract_media, media_generator, media_extractor
from src.downloader import fetch_m4a_audio
from src.utils.downloader import fullpipe

if __name__ == "__main__":

    processor = DataProcessor()
    balanced_dataset_path = Path("io/metadata/balanced_train_segments.csv")

    filter_keyword = "Neigh, whinny"

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
