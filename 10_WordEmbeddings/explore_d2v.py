import gensim
import logging
from icecream import ic
import json
from gensim.models import Doc2Vec
from gensim.models import KeyedVectors

file = open(r"C:\Users\lukas\Downloads\affairs.json", 'r', encoding='utf-8')
data = json.load(file)

model = Doc2Vec.load('affairs.d2v')
result = model.dv.most_similar(["Riem Katja"], topn=10)
word_vectors = model.wv

ic(word_vectors.get_index("europa"))
ic(word_vectors.keys())

ic(word_vectors.get_vecattr(key=result[0][0], attr="tag"))

file.close()
