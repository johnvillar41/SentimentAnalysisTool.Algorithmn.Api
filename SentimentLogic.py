from flask import jsonify
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from SentiwordModel import SentiwordModel
from TextCleaning import TextCleaning
from VaderModel import VaderModel
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.corpus import stopwords
lemmatizer = WordNetLemmatizer()


class SentimentLogic:

    @staticmethod
    def applyVader(sentence):
        sid_obj = SentimentIntensityAnalyzer()
        sentiment_dict = sid_obj.polarity_scores(sentence)

        negativeVal = sentiment_dict['neg']*100
        neutralVal = sentiment_dict['neu']*100
        positiveVal = sentiment_dict['pos']*100
        compoundVal = sentiment_dict['compound']*100
        compoundScore = ""
        if sentiment_dict['compound'] >= 0.05:
            compoundScore = "Positive"

        elif sentiment_dict['compound'] <= - 0.05:
            compoundScore = "Negative"

        else:
            compoundScore = "Neutral"

        vaderModel = VaderModel(negativeVal, positiveVal,
                                neutralVal, compoundScore, compoundVal)
        return vaderModel.toJSON()

    @staticmethod
    def applyHybrid(sentence):
        pass

    @staticmethod
    def applySentiWordNet(text):
        polarity = 0.0
        positiveScore = 0.0
        negativeScore = 0.0
        sentimentScore = ""

        _lemmas = TextCleaning.overallTextCleaning(text)
        print(_lemmas)

        for lemma in _lemmas:
            synsets = wn.synsets(lemma)

            if not synsets:
                continue
            
            # Grading of polarity
            synset = synsets[0]
            print(synset)
            swn_synset = swn.senti_synset(synset.name())

            positiveScore += swn_synset.pos_score()
            negativeScore += swn_synset.neg_score()
            polarity += swn_synset.pos_score() - swn_synset.neg_score()

        if polarity > 0:
            sentimentScore = "Positive"
        elif polarity == 0:
            sentimentScore = "Neutral"
        else:
            sentimentScore = "Negative"

        return SentiwordModel(polarity*100, positiveScore*100, negativeScore*100, sentimentScore).toJSON()
