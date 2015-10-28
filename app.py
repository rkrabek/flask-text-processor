import flask
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import nltk
import nltk.data
from nltk.tokenize import sent_tokenize, word_tokenize
import collections
import re
import os

# nltk.download()
app = Flask(__name__)
api = Api(app)

#HELPER FUNCTIONS
#################

def isWord(token):
    #allows contractions, titles, and hyphenated words
    if token.isalpha() or "'" in token or "." in token or "-" in token:
        #checking for tokenized single quotation marks or periods
        if token != "'" and token != ".":
            return True
    return False

#returns an array of total char count and total word count
def countWords(word_tokens):
    word_count = 0
    char_count = 0
    for word_token in word_tokens:
        if isWord(word_token):
            word_count += 1
            char_count += len(word_token)
    return [char_count, word_count]
    
#tokenizes request data into words    
def wordTokenizeRequest(request):
    data = request.get_json(force=True)
    word_tokens = nltk.word_tokenize(data['text'].lower())
    return word_tokens

#first sorts by word frequency then alphabetically if there is a tie
def wordSortFreqAlpha(request):
    #returns array of tuples format: (word, frequency)
    freq_array = collections.Counter(wordTokenizeRequest(request))
    #sorted by freq
    common_array = freq_array.most_common()
    #ties sorted alphabetically
    word_array = [token for token in common_array if isWord(token[0])]
    return sorted(word_array, key=lambda tup: (-tup[1], tup[0]))

#ENDPOINTS
##########

class AvgWordLen(Resource):
    def post(self):
        word_tokens = wordTokenizeRequest(request)
        #returns [char_count, word_count]
        counts = countWords(word_tokens)
        avg_len = float(counts[0])/counts[1]
        json = {"word_avg_len" : round(avg_len, 2)}
        return flask.jsonify(json)
api.add_resource(AvgWordLen, '/words/avg_len')

class MostCommonWord(Resource):
    def post(self):
        ties_alpha_sorted = wordSortFreqAlpha(request)
        #returns array of word tuples tied for most frequent
        freq_ties = [word for word in ties_alpha_sorted if ties_alpha_sorted[0][1] in word]
        json = {"word_most_com" : freq_ties[0][0]}
        return flask.jsonify(json)
api.add_resource(MostCommonWord, '/words/most_com')

class MedianWord(Resource):
    def post(self):
        ties_alpha_sorted = wordSortFreqAlpha(request)
        #array of all the words with the same freq as median word
        median_freq_ties = [word for word in ties_alpha_sorted if (ties_alpha_sorted[(len(ties_alpha_sorted)/2)][1]) in word]
        #extract just the words
        median_words = res_list = [word[0] for word in median_freq_ties]
        json = {"word_median" : median_words}
        return flask.jsonify(json)
api.add_resource(MedianWord, '/words/median')

class AvgSentenceLen(Resource):
    def post(self):
        data = request.get_json(force=True)
        word_count = 0
        #tokenizes request into sentences
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        sent_tokens = sent_detector.tokenize(data['text'].strip())
        #loops through each sentence and counts total words combined
        for sent_token in sent_tokens:
            word_tokens = nltk.word_tokenize(sent_token)
            word_count += countWords(word_tokens)[0]
        avg_len = float(word_count)/len(sent_tokens)
        json = {"sent_avg_len" : round(avg_len, 2)}
        return flask.jsonify(json)
api.add_resource(AvgSentenceLen, '/sentences/avg_len')

class Phones(Resource):
    def post(self):
        data = request.get_json(force=True)
        #regex from top answer at http://stackoverflow.com/questions/4111207/python-conditionally-delete-elements-from-list
        regex = ur"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
        phone_numbers = re.findall(regex, data['text'])
        json = {"phones" : phone_numbers}
        return flask.jsonify(json)
api.add_resource(Phones, '/phones')

if __name__ == "__main__":
    app.debug = True
    
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    app.logger.info("Starting flask app on %s:%s", host, port)

    app.run(host=host, port=port)