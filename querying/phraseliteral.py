from indexing.postings import Posting
from .querycomponent import QueryComponent

class PhraseLiteral(QueryComponent):
    """
    Represents a phrase literal consisting of one or more terms that must occur in sequence.
    """

    def __init__(self, terms : list[QueryComponent]):
        self.literals = terms

    def get_postings(self, index) -> list[Posting]:
        # Start normal interset (AND) merge between two terms
        # when two lists have the same document ID, do another intersection on positions.
        return None
        
    def __str__(self) -> str:
        return '"' + " ".join(map(str, self.literals)) + '"'