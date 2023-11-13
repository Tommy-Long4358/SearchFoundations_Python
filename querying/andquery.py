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
        # TODO: program the merge for an AndQuery, by gathering the postings of the composed QueryComponents and
		# intersecting the resulting postings.
        results = []

        recent_term_posting_list = self.components[0].get_postings(index)

        for i in range(1, len(self.components)):
            next_posting_list = self.components[i].get_postings(index)

            index1, index2 = 0, 0

            while index1 < len(recent_term_posting_list) and index2 < len(next_posting_list):
                # Check if IDs are equal to each other or not
                if recent_term_posting_list[index1].doc_id == next_posting_list[index2].doc_id:
                    new_position_list = []

                    for position1 in recent_term_posting_list[index1].position_list:
                        for position2 in next_posting_list[index2].position_list:
                            if position1 not in new_position_list:
                                new_position_list.append(position1)
                            
                            if position2 not in new_position_list:
                                new_position_list.append(position2)

                    if len(new_position_list) > 0:
                        #print(recent_term_posting_list[index1].doc_id, new_position_list)
                        results.append(Posting(recent_term_posting_list[index1].doc_id, new_position_list))

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
        
        return results

    def __str__(self):
        return " AND ".join(map(str, self.components))