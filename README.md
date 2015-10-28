# flask-text-processor
An API which takes json POST requests and can return various statistics about the text passed in

IMPORTANT
curl request must formatted:
curl -X POST -H "Content-type: application/json" -d '{"text":"My cat is gray. It doesn\u0027t have feathers."}' https://text-processor-flask-rkrabek.c9.io/words/avg_len
If malformed json is passed in such as "{'text':'My cat is gray.'}" the request will not work
Requests have only been tested with unicode characters due to shell configuration so for apostrophes, if executing from terminal, use \u0027

A word is considered any tokenization of alphabetical strings by nltk including:
- hyphenated (co-operation)
- contracted (n't or 'till)
- titles (Mr. or Mrs.)
Capitalized words are grouped with non capitalized words when determining frequency

Sentences are tokenized by periods which are not included in titles. 
Sentences may be tokenized even without capitalization of the new sentence.

Phone number formats supported include:
- 000-000-0000
- 000 000 0000
- 000.000.0000

- (000)000-0000
- (000)000 0000
- (000)000.0000
- (000) 000-0000
- (000) 000 0000
- (000) 000.0000

- 000-0000
- 000 0000
- 000.0000

- 0000000
- 0000000000
- (000)0000000
regex from http://stackoverflow.com/questions/3868753/find-phone-numbers-in-python-script