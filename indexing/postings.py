class Posting:
    """A Posting encapulates a document ID associated with a search query component."""
    def __init__(self, doc_id : int, position_list: list[int]):
        self.doc_id = doc_id
        self.position_list = position_list

    def add_position(self, position):
        self.position_list.append(position)