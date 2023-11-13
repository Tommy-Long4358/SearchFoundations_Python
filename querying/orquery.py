from .querycomponent import QueryComponent
from indexing import Index, Posting

from querying import querycomponent 

class OrQuery(QueryComponent):
    def __init__(self, components : list[QueryComponent]):
        self.components = components

    '''
    Retrieve first two components from self.components, do an OR intersection on the IDs and then another intersection if the IDs are similar.
    '''
    def get_postings(self, index : Index) -> list[Posting]:
        results = []

        # Get first component
        recent_term_posting_list = self.components[0].get_postings(index)

        for i in range(1, len(self.components)):
            # Retrieve next component
            next_posting_list = self.components[i].get_postings(index)

            # Index variables to traverse through two lists
            index1, index2 = 0, 0

            # Loop until one list is fully traversed
            while index1 < len(recent_term_posting_list) and index2 < len(next_posting_list):
                # Check if IDs are equal to each other or not
                if recent_term_posting_list[index1].doc_id == next_posting_list[index2].doc_id:
                    new_position_list = []

                    # Merge position lists into one list, sorted in order
                    for position1 in recent_term_posting_list[index1].position_list:
                        for position2 in next_posting_list[index2].position_list:
                            if position1 not in new_position_list:
                                new_position_list.append(position1)
                            
                            if position2 not in new_position_list:
                                new_position_list.append(position2)

                    new_position_list = sorted(new_position_list)

                    # Only add the combined position list if there is atleast more than one position in either list
                    if len(new_position_list) > 0:
                        #print(recent_term_posting_list[index1].doc_id, new_position_list)
                        results.append(Posting(recent_term_posting_list[index1].doc_id, new_position_list))

                    # Append both indexes
                    index1 += 1
                    index2 += 1
                
                elif recent_term_posting_list[index1].doc_id > next_posting_list[index2].doc_id:
                    # If one ID is bigger than the other, we go to the next element in the list with the lowest element
                    results.append(next_posting_list[index2])
                    index2 += 1

                else:
                    results.append(recent_term_posting_list[index1])
                    index1 += 1
            
            # For any list that wasn't fully traversed, we add its remaining contents to results
            if index1 < len(recent_term_posting_list):
                results += recent_term_posting_list[index1:len(recent_term_posting_list)]

            elif index2 < len(next_posting_list):
                results += next_posting_list[index2:len(next_posting_list)]
            
            if len(results) > 1:
                # Update posting list to be compared 
                recent_term_posting_list = results[len(results) - 1]
        
        return results

    def __str__(self):
        return "(" + " OR ".join(map(str, self.components)) + ")"