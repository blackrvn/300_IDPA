import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import unique
from gensim.models import Doc2Vec
from icecream import ic
from sklearn.manifold import TSNE
from utils import get_details_by_cname
from utils import interested_parties

tsne = TSNE(n_components=3, random_state=0, perplexity=5)

model = Doc2Vec.load(r'DocModels\tag_party_test.d2v')
party_vectors = np.array([model.dv[p] for p in interested_parties])
councillor_vectors = np.array([model.dv[p] for p in model.dv.index_to_key if p not in interested_parties])
councillor_labels = [label for label in model.dv.index_to_key if label not in interested_parties]
parties = [p for p in model.dv.index_to_key if p in interested_parties]

reduced_party_vectors = tsne.fit_transform(party_vectors)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
for i, v in enumerate(reduced_party_vectors):
    ax.scatter(v[0], v[1], v[2], label=parties[i])

plt.legend()
plt.show()

sims = {}

for idx, vector in enumerate(party_vectors):
    sim = model.dv.cosine_similarities(vector, party_vectors)
    party = interested_parties[idx]
    sims[party] = {}
    for i, s in enumerate(sim):
        p = interested_parties[i]
        if party != p:
            sims[party][p] = round(s, 2)

ic(sims)

sims_councillors = {}


def calculate_accuracy(dictionary):
    correct = 0
    total = 0

    for person, data in dictionary.items():
        actual_party = data['Zugehörigkeit']
        similarities = data['Ähnlichkeiten']

        # Find the parties with the two highest similarities
        predicted_parties = sorted(similarities, key=similarities.get, reverse=True)[:2]

        # If one of the predicted parties is the same as the actual party, increment correct
        if actual_party in predicted_parties:
            correct += 1

        total += 1

    # Calculate accuracy
    accuracy = correct / total

    return accuracy


for idx, councillor in enumerate(councillor_vectors):
    sims = model.dv.cosine_similarities(councillor, party_vectors)
    l = {}
    for i, s in enumerate(sims):
        party = interested_parties[i]
        l[party] = round(s, 2)
    name = councillor_labels[idx]
    counc_party = get_details_by_cname(name)["party"]
    sims_councillors[name] = {"Zugehörigkeit": counc_party, "Ähnlichkeiten": l}

ic(sims_councillors)
ic(calculate_accuracy(sims_councillors))
