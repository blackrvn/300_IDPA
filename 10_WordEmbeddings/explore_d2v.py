import json

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pandas as pd
from gensim.models import Doc2Vec
from icecream import ic
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, random_state=0)

interested_parties = ["SP", "SVP", "FDP-Liberale", "glp", "GRÜNE", "M-E"]

NUM_CLUSTERS = len(interested_parties)

model_parties = Doc2Vec.load('tag_party.d2v')
party_vectors = model_parties.dv.vectors
parties = [p for p in model_parties.dv.index_to_key if p in interested_parties]
num_parties = len(party_vectors)

model_councillors = Doc2Vec.load('tag_councillor.d2v')
councillors_vectors = model_councillors.dv.vectors

reduced_councillor_vectors = tsne.fit_transform(councillors_vectors)
reduced_party_vectors = tsne.fit_transform(councillors_vectors)
ic(reduced_party_vectors)

councillor_names = model_councillors.dv.index_to_key
kmeans_councillors = KMeans(n_clusters=NUM_CLUSTERS, random_state=0)
kmeans_councillors.fit(reduced_councillor_vectors)
labels_councillors = kmeans_councillors.labels_


def get_details_by_cname(name):
    with open("councillor_details.json", "r") as file:
        json_data = json.load(file)
        return json_data[name]


parties_by_person = []
for person in councillor_names:
    parties_by_person.append(get_details_by_cname(person)["party"])

df = pd.DataFrame({
    'Label': labels_councillors,
    'Name': councillor_names,
    'Party': parties_by_person
})

fig, (ax0, ax1, ax2) = plt.subplots(nrows=1, ncols=3, figsize=(15, 10))

color_list = list(mcolors.TABLEAU_COLORS.keys())

label_colors = {}
for i in set(labels_councillors):
    label_colors[i] = color_list[i]

handles_0 = []
for i in set(labels_councillors):
    df_query = df.query("Label == @i")
    for index, row in df_query.iterrows():
        h = ax0.scatter(reduced_councillor_vectors[index][0], reduced_councillor_vectors[index][1], label=i, c=label_colors[i])
    handles_0.append(h)

l0 = ax0.legend(
                loc='lower left',
                title='Clusters',
                labels=set(labels_councillors),
                handles=handles_0,
                ncols=2,
                # bbox_to_anchor=(0, -0.15, 0, 0)
                )

handles_1 = []

for i, party in enumerate(interested_parties):
    df_query = df.query("Party == @party")
    for index, row in df_query.iterrows():
        h = ax1.scatter(reduced_councillor_vectors[index][0], reduced_councillor_vectors[index][1], label=party, c=label_colors[i])
    handles_1.append(h)

l1 = ax1.legend(
                loc='lower left',
                title='Partliche verteilung',
                labels=interested_parties,
                handles=handles_1,
                ncols=2,
                # bbox_to_anchor=(0, -0.15, 0, 0)
                )

handles_2 = []

for i, party in enumerate(parties):
    if party in interested_parties:
        h = ax2.scatter(reduced_party_vectors[i][0], reduced_party_vectors[i][1], label=party, c=label_colors[i])
        handles_2.append(h)

l1 = ax2.legend(
                loc='lower left',
                title='Partliche verteilung',
                labels=interested_parties,
                handles=handles_1,
                ncols=2,
                # bbox_to_anchor=(0, -0.15, 0, 0)
                )

plt.show()

cluster_councillor_map = {}

for idx, cv in enumerate(reduced_councillor_vectors):
    pred = kmeans_councillors.predict(cv.reshape(1, -1))
    if pred[0] in cluster_councillor_map.keys():
        cluster_councillor_map[pred[0]].append(get_details_by_cname(councillor_names[idx]))
    else:
        cluster_councillor_map[pred[0]] = [get_details_by_cname(councillor_names[idx])]

ic(cluster_councillor_map)
