'''
Write a new derived-class of TokenProcessor that processes tokens 
into types and normalizes types into terms with two different methods. The "process token" method should convert a 
token into a type by:

If there is at least one hyphen (-) in the token:
    - Split the token to form 2 or more tokens.
    - Form a set containing the split tokens, as well as the original token with the hypen(s) removed.

Example: "Hewlett-Packard-Computing" turns into the set {Hewlett, Packard, Computing, HewlettPackardComputing}.
The remaining steps are performed on each token in the set, and the set of resulting types is returned. 
Note that this means the "process token" method now returns a list of string results, not just a single string.

Remove all non-alphanumeric characters from the beginning and end of the token, but not the middle.
Example: Hello. becomes Hello ; 192.168.1.1 remains unchanged.

Remove all apostrophes or quotation marks (single or double quotes) from anywhere in the token.
Convert the token to lowercase.

Add a "normalize type" method to your TokenProcessor class, which converts a type into a term by:

- Stem the using a "Porter2 Stemmer". Please do not code this yourself; 
find an implementation with a permissible license and integrate it with your solution.

The terms are inserted into the inverted index. Types are only used for 
wildcard queries and spelling correction; they can be discarded if you are not implementing those.
'''
from .tokenprocessor import TokenProcessor
from porter2stemmer import Porter2Stemmer
import re

class TokenTypeProcessor(TokenProcessor):
    non_alphanumeric = re.compile(r'^\W+|\W+$')
    single_quotes = re.compile(r"'*'")
    double_quotes = re.compile(r'"*"')

    def process_token(self, token: str) -> list[str]:
        processed_token = set()

        # Remove all non-alphanumeric characters from beginning and end of the token, but not the middle
        token = re.sub(self.non_alphanumeric, "", token)

        # Remove all single quotes from anywhere in the token. 
        token = re.sub(self.single_quotes, "", token)

        # Convert token to lowercase and remove double quotes
        token = re.sub(self.double_quotes, "", token)
        # Add token to set 
        processed_token.add(token.lower())

        # Do splitting if a hypen exists
        if "-" in token:
            # Split token to form 2 or more tokens
            split_token = token.split("-")

            for token in split_token:
                # form a set containing the split tokens, as well as the original token with the hypen removed
                processed_token.add(token)

        # Return set of tokens
        return list(processed_token)

    '''
    Add a "normalize type" method to your TokenProcessor class, which converts a type into a term by:
        - Stem the using a "Porter2 Stemmer". Please do not code this yourself; 
        find an implementation with a permissible license and integrate it with your solution.

    The terms are inserted into the inverted index. Types are only used for 
    wildcard queries and spelling correction; they can be discarded if you are not implementing those.
    '''
    def normalize_type(self, type: str) -> str:
        stemmer = Porter2Stemmer()

        return stemmer.stem(type)