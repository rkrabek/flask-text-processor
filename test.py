import nltk.data
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

import re
regex = ur"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
line = "thingdsa arfe happening 000-000-0000 000 000 0000 000.000.0000 (000)000-0000 (000)000 0000 (000)000.0000"
person = re.findall(regex, line)
print(person)


# sentence = "Punkt knows that the periods in Mr. Smith and Johann S. Bach do not mark sentence boundaries.  And sometimes sentences can start with non-capitalized words."
# thing = "'"
# sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
# tokens = sent_detector.tokenize(sentence.strip())

# tokens = nltk.word_tokenize(sentence)
    
# print tokens

# def isWord(token):
#     #allows contractions, titles, and hyphenated words
#     if token.isalpha() or "'" in token or "." in token or "-" in token:
#         #checking for tokenized single quotation marks or periods
#         if token != "'" and token != ".":
#             return True
#     return False

# wordtokens = [token for token in tokens if isWord(token)]
# print wordtokens
# tokens = nltk.word_tokenize(sentence)
# if sentence.isalpha() or "'" in sentence:
#     print "stuff"

# if thing.isalpha() or "'" in thing:
#     if thing != "'":
#         print "yay"

# tuplestring = ('thingys', 5)
# print tuplestring[1]

# print tokens
# if "'" in sentence:
#     print "things"