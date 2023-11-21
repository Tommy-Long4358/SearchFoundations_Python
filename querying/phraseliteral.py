from indexing.postings import Posting
from .querycomponent import QueryComponent

class PhraseLiteral(QueryComponent):
    """
    Represents a phrase literal consisting of one or more terms that must occur in sequence.
    """

    def __init__(self, terms : list[QueryComponent]):
        self.literals = terms

    '''
    PhraseLiteral: contains a list of two or more query components that are expected to be in subsequent positions. Let k=1. 
    Retrieve postings for the first two components in the phrase, and look for documents that are in both similar to an AND merge. 
    If a document is found, examine the positions next, looking for a position in the first list that is equal to a position in the second list minus k. 
    If found, retain that document and the correct position(s). Like with an AndQuery, continue to get postings for each subsequent component in the phrase, 
    increasing k each loop. The book has an implementation of this algorithm in pseudocode.
    
    To answer a phrase query, start the normal intersect (AND) merge between the two terms. When two lists have the same document ID, do another intersection on the 
    positions, looking for positions off by one
    '''
    def get_postings(self, index) -> list[Posting]:
        results = []
        
        # Get initial literal's postings list
        recent_term_posting_list = self.literals[0].get_postings(index)

        # Variable for checking if terms are within k promixity of each other (for multiple words like "national park" or "sand creek massacre")
        k = 1
        for i in range(1, len(self.literals)):
            # Get next literal's postings list
            next_posting_list = self.literals[i].get_postings(index)

            index1, index2 = 0, 0
            while index1 < len(recent_term_posting_list) and index2 < len(next_posting_list):
                # Check if IDs are equal to each other or not
                if recent_term_posting_list[index1].doc_id == next_posting_list[index2].doc_id:
                    new_position_list = []

                    # Get position list of both postings lists
                    posting_lst1 = recent_term_posting_list[index1].position_list
                    posting_lst2 = next_posting_list[index2].position_list

                    # Pointer variable
                    index1_id, index2_id = 0, 0

                    while index1_id < len(posting_lst1):
                        while index2_id < len(posting_lst2):
                            # Check if two terms appear within k words of each other or less
                            # looks for a position in the first list that is equal to a position in the second list minus k
                            if abs(posting_lst1[index1_id] - posting_lst2[index2_id]) <= k:
                                # If found, retain that document and the correct position(s)
                                new_position_list.append(posting_lst2[index2_id])
                            
                            elif posting_lst2[index2_id] > posting_lst1[index1_id]:
                                break
                            
                            index2_id += 1

                        index1_id += 1    

                    # Only add document ID and position list if two terms appeared within k words of each other or less.
                    if len(new_position_list) > 0:
                        results.append(Posting(recent_term_posting_list[index1].doc_id, sorted(posting_lst1 + new_position_list)))

                    index1 += 1
                    index2 += 1

                elif recent_term_posting_list[index1].doc_id > next_posting_list[index2].doc_id:
                    # If one ID is bigger than the other, we go to the next element in the list with the lowest element
                    index2 += 1

                else:
                    index1 += 1

            if len(results) > 1:
                # Update posting list to be compared 
                recent_term_posting_list = results[len(results) - 1]
            
                k += 1
        
        return results
        
    def __str__(self) -> str:
        return '"' + " ".join(map(str, self.literals)) + '"'