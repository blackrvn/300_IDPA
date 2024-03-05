import spacy
import pickle
from corpora import *

model = spacy.load("de_dep_news_trf")
import de_dep_news_trf
import glob
import os

with open("corpora.pickle", "rb") as pickle_file:
    corpora = pickle.load(pickle_file)

affair_text_dict = corpora.get_text()

for affair_id, text in affair_text_dict.items():
    nlp = de_dep_news_trf.load()
    doc = nlp(text)
    no_punct = [token for token in doc if not
                token.is_punct and not token.is_digit and not token.is_currency and not token.is_bracket]
    affair_obj = corpora[affair_id]
    affair_obj.clean_text = no_punct
    
