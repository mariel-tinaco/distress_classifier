

from dataclasses import dataclass, field
from typing import List


@dataclass
class AudioClassification:
    id : str
    name : str
    description : str
    citation_uri : str
    positive_examples : List[str]
    child_ids : List[str]
    restrictions : List[str]


    




