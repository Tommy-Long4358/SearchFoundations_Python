'''
An inverted index is just another implementation of the Index interface. 
Decide on an appropriate way to associate terms with postings lists inside the 
inverted index class, then implement the getPostings(String) method and the 
getVocabulary() method (recall that getVocabulary() must return a sorted vocabulary list).
'''
from typing import Iterable
from .postings import Posting
from .index import Index

class InvertedIndex(Index):
    def __init__(self):
       # You should be using a dictionary that maps from string to a list of integer
       self.vocabulary = {}

    '''
    Postings lists must contain distinct document IDs (no ID can occur more than once). 
    When tokenizing and indexing a document, it's possible that you will find a term in a 
    document that you have already seen before, and so that document ID already occurs in 
    the postings list for that term. You must take care to not insert that document ID a second 
    time into the postings list in the addTerm method.

    Your implementation of addTerm must run in O(1) time. This means you cannot call a method like 
    .find(), .contains(), .indexOf(), "in", etc., and cannot write a loop over each index in a 
    postings list. Those methods run in O(n) time.
    
    Time bound can be achieved by observing that documents are indexed in increasing order by ID. Whatever document is currently
    being indexed has the largest ID of any document seen so far. Therefore, if the current document is already in the index for a term,
    where would you find it in the postings list?
    '''
    def add_term(self, term : str, doc_id : int):
        '''
        My terrible solution:
        # If term doesn't exist in dictionary, assign it a set() to contain all unique document IDs.
        if not self.vocabulary.get(term):
            self.vocabulary[term] = set()

        # Add document ID associated with term to dictionary. Sets automatically ignore any duplicate elements.
        self.vocabulary[term].add(Posting(doc_id))
        '''

        posting_list = self.vocabulary.get(term)

        # If statement implies that there is no Posting doc ids in the list.
        if not posting_list:
            # Initialize key for a given term.
            self.vocabulary[term] = []

            # Append to list.
            self.vocabulary[term].append(Posting(doc_id))
    
        elif posting_list[len(posting_list) - 1].doc_id != doc_id:
            # Else statement implies the list of integers is not empty and we must check if the doc_id exists in the list or not.

            # Since the documents are indexed in increasing order and are appended in increasing order, we can check the last element 
            # in the postings list to see if a given document ID already exists or not.
            self.vocabulary[term].append(Posting(doc_id))
    

    def get_postings(self, term : str) -> Iterable[Posting]:
        """Retrieves a sequence of Postings of documents that contain the given term."""
        return self.vocabulary.get(term)

    def vocabulary(self) -> list[str]:
        """A (sorted) list of all terms in the index vocabulary."""
        return self.vocabulary.keys().sort()

