import numpy as np
from icecream import ic
from utils import get_details_by_cname
from utils import interested_parties

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from gensim.models import Doc2Vec
from sklearn.metrics.pairwise import cosine_similarity
import numpy

import json

model = Doc2Vec.load(r"DocModels/tag_councillor.d2v")

councillor_vectors = model.dv.vectors
ic(len(councillor_vectors))
councillors_by_party = {}

councillor_labels = model.dv.index_to_key
parties = [get_details_by_cname(c)["party"] for c in councillor_labels]
centroids = {}
for i, prty in enumerate(parties):
    if prty in councillors_by_party.keys():
        councillors_by_party[prty].append(councillor_labels[i])
    else:
        councillors_by_party[prty] = [councillor_labels[i]]

for i, party in enumerate(interested_parties):
    all_vectors_by_party = np.array([v for i, v in enumerate(councillor_vectors) if parties[i] == party])
    centroid = KMeans(n_clusters=1, random_state=0).fit(all_vectors_by_party).cluster_centers_.reshape(70,)
    centroids[party] = centroid

model.dv.add_vectors(list(centroids.keys()), list(centroids.values()))

sims = {}

for party in centroids:
    sim = model.dv.cosine_similarities(model.dv[party], np.array(list(centroids.values())))
    l = {"Parteien": {}, "Politiker": {}}
    for i, s in enumerate(sim):
        p = list(centroids.keys())[i]
        if p != party:
            l["Parteien"][p] = s

    """
    for cs in [cs for cs in model.dv.similar_by_key(party, len(model.dv)) if cs[0] in councillors_by_party[party]]:
        most_similar = [part for part in model.dv.similar_by_key(cs[0], len(model.dv)) if part[0] in interested_parties]
        l["Politiker"][cs[0]] = most_similar[0][0]

    """
    sims[party] = l

ic(sims)
