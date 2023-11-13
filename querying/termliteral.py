from indexing.postings import Posting
from .querycomponent import QueryComponent

class TermLiteral(QueryComponent):
    """
    A TermLiteral represents a single term in a subquery.
    """

    def __init__(self, term : str):
        self.term = term

    """ To getPostings, we simply go to the provided Index and retrieve the postings for the TermLiteral object's string."""
    def get_postings(self, index) -> list[Posting]:
        posting_list = index.get_postings(self.term)

        return posting_list if posting_list else []
    
    def __str__(self) -> str:
        return self.term