
from dataclasses import dataclass, field
import dataclasses
from io import TextIOWrapper
from typing import Dict, List, Union
from pathlib import Path
import json


@dataclass
class AudiosetClass:
    """ Data representation of audio classes from Audio Dataset ontology
    
    Reference: https://github.com/audioset/ontology

    :param id: The machine identifier for this class
    :type str: 
    :param name: The Display Name that refers to the class.
    :type str:
    :param description: A description of the class in a few lines.
    :type str: 
    :param citation_uri: A pointer to any text used as the basis for    \
        the description. 
    :type str:
    :param positive_examples: A list of compact URLs to segments within \
        YouTube files that provide confirmed positive examples of this class.
    :type List[str]: List of URL strings 
    :param child_ids: A list of the id fields for any classes that      \
        children of this class in the class hierarchy.
    :type List[str]: List of id fields
    :param child_ids:  A list of the id fields for any classes that     \
        children of this class in the class hierarchy.
    :type List[str]: List of id strings
    :param restrictions: A list that can include the following values: 
        abstract -> for a class that is principally a container within  \
            the hierarchy, but will not have any explicit examples for  \
            itself.
        blacklist -> for classes that have been excluded from rating for \
            the time being. 

    """

    id : str
    name : str
    description : str
    citation_uri : str
    positive_examples : List[str]
    child_ids : List[str]
    restrictions : List[str]


def extract_audioset (file : Union[Path, str, TextIOWrapper], key : int) -> Dict[str, AudiosetClass]:
    """ Load Ontology from JSON file
    
    :param file: Source file
    :type Union[Path, str, TextIOWrapper]:
    :param key: Select key type
        0 -> id
        1 -> name

    :return Dict[str, AudiosetClass]:
    """

    if isinstance (file, TextIOWrapper):
        ontology = json.load(file)

    else:
        with open(file, "r") as infile:
            ontology = json.load(infile)

    data = dict()

    for item in ontology:
        audioclass = AudiosetClass (
            id = item["id"],
            name = item["name"],
            description= item["description"],
            citation_uri= item["citation_uri"],
            positive_examples=item["positive_examples"],
            child_ids= item["child_ids"],
            restrictions= item["restrictions"]
        )
        if key == 1:
            data[item["name"]] = dataclasses.asdict(audioclass)
        else:
            data[item["id"]] = dataclasses.asdict(audioclass)

    return data

if __name__ == "__main__":

    # with open(Path("ontology/ontology.json"), "r") as file:
    #     data = extract_audioset(file)

    data = extract_audioset(file=Path("ontology/ontology.json"), key=1)
    print(json.dumps(data, indent=3))