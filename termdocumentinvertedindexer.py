from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, PositionalInvertedIndex
from text import TokenTypeProcessor, englishtokenstream
from querying import BooleanQueryParser

def index_corpus(corpus : DocumentCorpus) -> Index:
    # An object that can transform a token (string from document) into a term (processed, normalized token)
    token_processor = TokenTypeProcessor()
    term_document_positional_inverted_index = PositionalInvertedIndex()
    
    for d in corpus:
        # Load all documents on corpus
        print(f"Found document {d.title}")
        
        # Tokenize the document's content by creating an EnglishTokenStream around the document's .content()
        tokenized_document = englishtokenstream.EnglishTokenStream(d.get_content())

        # Iterate through the token stream, processing each with token_processor's process_token method.
        for index, token in enumerate(tokenized_document):
            terms = token_processor.process_token(token)

            for term in terms:
                # Add the processed token (a "term") to the inverted indexs
                term_document_positional_inverted_index.add_term(term, d.id, index)
    
    return term_document_positional_inverted_index

if __name__ == "__main__":
    # Folder name input
    #folder = str(input("Enter folder name: "))
    #corpus_path = Path(folder)

    # File type input
    #file_type = str(input("Enter type of file: "))

    # Load corpus from given folder path and file type
    d = DirectoryCorpus.load_text_directory("NPS", ".json")

    # Construct a corpus
    index = index_corpus(d)

    # parser for queries
    query_parser = BooleanQueryParser()

    # Build the index over this directory.
    while True:
        menu_num = int(input("\nMenu:\n1. Search Word\n2. Quit\nEnter an option: "))

        if menu_num == 1:
            query = str(input("Enter a term to search: "))

            query_type = query_parser.parse_query(query)

            print(query_type)
            print("\nSearch Results:")

            # Has to be of Posting type
            for posting in query_type.get_postings(index):
                print(f"Document Name: {d.get_document(posting.doc_id).title}.txt")

            if not query_type.get_postings(index):
                print("No results found!")

        elif menu_num == 2:
            print("Bye!")
            break
        else:
            print("Not a valid option! Try again.")