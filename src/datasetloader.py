from typing import List
from dataclasses import dataclass


@dataclass
class Media:
    """ Media Info

    """
    url : str
    start : float
    stop : float
    tags : List[str]
