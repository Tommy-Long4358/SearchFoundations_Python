from typing import Iterable
from .postings import Posting
from .index import Index
'''
You will maintain one index for your corpus: the PositionalInvertedIndex, a positional index as discussed in class, 
where postings lists consist of (documentID, [position1, position2, ...]) pairs. Using InvertedIndex from Homework 2 as 
a reference point, create PositionalInvertedIndex as a new implementation of the Index interface. We will no longer 
have a need for positionless postings, so the Posting class will need to be updated to represent the list of positions 
of a posting. You will also need to modify addTerm to account for the position of the term within the document. 

The index should consist of a hash map from string keys (the terms in the vocabulary) to (array) lists of postings. 
You must not use any other hash maps or any “set” data structures in your code, only lists.
'''
class PositionalInvertedIndex(Index):
    def __init__(self):
       self.vocabulary = {}

    ''' 
    postings list consists of (documentID, [position1, position2, ...]) pairs 
    
    represented as [(documentID, [position1, position2, ...]), (documentID, [position1, position2, ...]), (documentID, [position1, position2, ...])]?
    '''
    def add_term(self, term : str, doc_id : int, position : int):
        posting_list = self.vocabulary.get(term)

        # If statement implies that there is no Posting list for a given term
        if not posting_list:
            # Initialize key for a given term and add in position to list
            self.vocabulary[term] = [Posting(doc_id, [position])]

        elif posting_list[len(posting_list) - 1].doc_id == doc_id:
            # If the ID is still the same as the most recent posting ID, we add its position to it
            self.vocabulary.get(term)[len(posting_list) - 1].add_position(position)
        
        else:
            # If the ID is different, we make a new Posting object
            self.vocabulary[term].append(Posting(doc_id, [position]))
    
    def get_postings(self, term : str) -> Iterable[Posting]:
        """Retrieves a sequence of Postings of documents that contain the given term."""
        return self.vocabulary.get(term)

    def vocabulary(self) -> list[str]:
        """A (sorted) list of all terms in the index vocabulary."""
        return self.vocabulary.keys().sort()