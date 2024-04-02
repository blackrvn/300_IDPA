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
from utils import calculate_accuracy
from utils import get_num_councillors

tsne = TSNE(n_components=3, random_state=0, perplexity=5)

model = Doc2Vec.load(r'DocModels\tag_party_geq51.d2v')
party_vectors = np.array([model.dv[p] for p in interested_parties])
ic(party_vectors[0].shape)
councillor_vectors = np.array([model.dv[p] for p in model.dv.index_to_key if p not in interested_parties])
councillor_labels = [label for label in model.dv.index_to_key if label not in interested_parties]
parties = [p for p in model.dv.index_to_key if p in interested_parties]

reduced_party_vectors = tsne.fit_transform(party_vectors)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
for i, v in enumerate(reduced_party_vectors):
    ax.scatter(v[0], v[1], v[2], label=parties[i])

plt.legend()
# plt.show()

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

avg_similarities = []

for prt in interested_parties:
    num = len([councillor for councillor in sims_councillors if sims_councillors[councillor]["Zugehörigkeit"] == prt])
    res = np.array([sims_councillors[councillor]["Ähnlichkeiten"][party] for councillor in sims_councillors for party in interested_parties if sims_councillors[councillor]["Zugehörigkeit"] == prt])
    res = res.reshape(num, len(interested_parties))
    avg_similarities.append(res)

avg_similarities = [np.mean(arr, axis=0) for arr in avg_similarities]
# Create bar chart

party_colors = {
    'FDP-Liberale': 'b',
    'GRÜNE': 'g',
    'M-E': 'orange',
    'SP': 'r',
    'SVP': 'c',
    'glp': 'y'
}

# Create bar chart with grouped bars and different colors
plt.figure(figsize=(10, 6))
bar_width = 0.15
x = np.arange(len(interested_parties))

for i, party in enumerate(interested_parties):
    plt.bar(x + i * bar_width, avg_similarities[i], bar_width, label=party, color=party_colors[party])

plt.xlabel('Parteien')
plt.ylabel('Durchschnittliche Ähnlichkeit')
plt.xticks(x + bar_width * 2.5, interested_parties, rotation=45, ha='right')
plt.legend()
plt.text(1, 0.4, f"Genauigkeit: {round(calculate_accuracy(sims_councillors)*100, 1)}%")
plt.tight_layout()

# Save the chart as an image
plt.savefig(r"C:\Users\lukas\Documents\300_IDPA\09_Quellen\Plots\Q1_SimByParty_L51.png")

# Show the chart
plt.show()


