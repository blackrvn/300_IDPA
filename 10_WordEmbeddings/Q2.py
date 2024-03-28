import json

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pandas as pd
from numpy import unique
from gensim.models import Doc2Vec
from icecream import ic
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.cluster import AgglomerativeClustering
from utils import get_details_by_cname
from utils import interested_parties
import gensim

tsne = TSNE(n_components=3, random_state=0, perplexity=5)
model = Doc2Vec.load(r'DocModels\tag_party.d2v')
doc_vectors = model.dv

with open("test_data.json", encoding="utf-8", mode="r") as test_file:
    test_data = json.load(test_file)

docs = [test_data[affair] for affair in test_data]

sims_unseen_affairs = {}
num_right = 0

for i, a in enumerate(test_data):
    vec = model.infer_vector(test_data[a][0])
    sims = model.dv.similar_by_vector(vec, topn=2)
    expected = test_data[a][1][0]
    calculated = [sims[0][0], sims[1][0]]
    sims_unseen_affairs[a] = {"Expected": expected, "Calculated": calculated}
    if expected in calculated:
        num_right += 1

total = len(sims_unseen_affairs.keys())
ic(round(num_right/total, 2))
