'''
Your search engine should ask for a directory to load documents from when it begins. You should be able to load both 
.txt documents (as in the homework) and also .json documents; your project will be tested with the corpus contained 
in this ZIP file Download this ZIP fileOpen this document with ReadSpeaker docReader, which contains over 30,000 documents 
I copied from the National Parks Service website many years ago.

JSON documents are very different than the Moby Dick text documents: their title and content are both pulled from specific 
keys in the JSON data, rather than the content being the entire byte content of the file. This page will walk you through 
writing a JsonFileDocument class and using it to load .json documents into your existing search engine.
'''

import json
from .document import Document
from typing import Iterable
from pathlib import Path
import io

class JsonFileDocument(Document):
    """
    Represents a JSON document that will be loaded into the search engine.
    """
    def __init__(self, doc_id: int, path: Path):
        super().__init__(doc_id)
        self.path = path

    @property
    def title(self) -> str:
        return self.path.stem
    
    # Because its a JSON file, we need to grab its contents differently as compared to a .txt file
    def get_content(self) -> Iterable[str]:
        """Gets an iterable sequence over the content of the document."""
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data.get("body").split(" ")

    @staticmethod
    def load_from(abs_path : Path, doc_id : int) -> 'JsonFileDocument' :
        """A factory method to create a JsonFileDocument around the given file path."""
        return JsonFileDocument(doc_id, abs_path)