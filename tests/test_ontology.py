import sys, os
import json
from pathlib import Path

sys.path.append(os.path.join(os.getcwd(), "."))

from src.ontology import extract_audioset

# Extract control data
path = Path("ontology/ontology.json")
with open(path, "r") as file:
    control_data = json.load(file)


def test_length():
    """ Match length of external ontology source and extracted audio set
    
    """
    audioset_data = extract_audioset(path, key=1)
    assert len(control_data) == len(audioset_data)

