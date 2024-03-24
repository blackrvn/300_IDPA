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

tsne = TSNE(n_components=3, random_state=0, perplexity=5)

model_parties = Doc2Vec.load(r'DocModels\tag_party_part.d2v')
party_vectors = model_parties.dv.vectors
parties = [p for p in model_parties.dv.index_to_key if p in interested_parties]

reduced_party_vectors = tsne.fit_transform(party_vectors)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
for i, v in enumerate(reduced_party_vectors):
    ax.scatter(v[0], v[1], v[2], label=parties[i])

plt.legend()
plt.show()

sims = {}

for i, party in enumerate(parties):
    self_vector = party_vectors[i]
    sim = model_parties.dv.similar_by_vector(self_vector)
    sim.pop(0)
    sims[party] = {}
    for s in sim:
        sims[party][s[0]] = round(s[1], 2)

ic(sims)

