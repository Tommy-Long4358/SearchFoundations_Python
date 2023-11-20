from .querycomponent import QueryComponent
from indexing import Index, Posting

from querying import querycomponent 

class AndQuery(QueryComponent):
    '''
    stores a list of two or more query components, whose postings must be merged with 
    the "AND" merge.
    '''
    def __init__(self, components : list[QueryComponent]):
        # please don't rename the "components" field.
        self.components = components

    '''
    We must get the postings of the first two query components 
    contained in the AndQuery, then merge them with the algorithm from lecture. If there is another query component, 
    we retrieve its postings and merge it with the previous result. Repeat this process until all the components 
    contained in the AndQuery have been merged.
    '''
    def get_postings(self, index : Index) -> list[Posting]:
        results = []
        
        # Starting posting list
        recent_term_posting_list = self.components[0].get_postings(index)

        for i in range(1, len(self.components)):
            # ith posting list to compare to starting posting list
            next_posting_list = self.components[i].get_postings(index)

            index1, index2 = 0, 0
            
            while index1 < len(recent_term_posting_list) and index2 < len(next_posting_list):
                # Check if IDs are equal to each other or not
                if recent_term_posting_list[index1].doc_id == next_posting_list[index2].doc_id:
                    new_position_list = sorted(recent_term_posting_list[index1].position_list + next_posting_list[index2].position_list)
                    
                    #TODO: What to do with position list?? AND all positions?
                    results.append(Posting(recent_term_posting_list[index1].doc_id, new_position_list))

                    index1 += 1
                    index2 += 1
                
                elif recent_term_posting_list[index1].doc_id > next_posting_list[index2].doc_id:
                    # If one ID is bigger than the other, we go to the next element in the list with the lowest element
                    index2 += 1

                else:
                    index1 += 1

            # Only update starting posting list if results were found for both terms
            if len(results) > 1:
                # Set starting posting list to merged posting list
                recent_term_posting_list = results[len(results) - 1]
        
        return results

    def __str__(self):
        return " AND ".join(map(str, self.components))