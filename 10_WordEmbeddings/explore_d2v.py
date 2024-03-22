import json

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import unique
from numpy import where
from gensim.models import Doc2Vec
from icecream import ic
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.cluster import AgglomerativeClustering

from query_json import interested_parties

tsne = TSNE(n_components=2, random_state=0)

NUM_CLUSTERS = len(interested_parties)

model_parties = Doc2Vec.load('tag_party.d2v')
party_vectors = model_parties.dv.vectors
parties = [p for p in model_parties.dv.index_to_key if p in interested_parties]
num_parties = len(party_vectors)

model_councillors = Doc2Vec.load('tag_councillor_1970.d2v')
councillors_vectors = model_councillors.dv.vectors

reduced_councillor_vectors = tsne.fit_transform(councillors_vectors)
reduced_party_vectors = tsne.fit_transform(councillors_vectors)

councillor_names = model_councillors.dv.index_to_key
kmeans_councillors = KMeans(n_clusters=NUM_CLUSTERS, random_state=0)
kmeans_councillors.fit(councillors_vectors)
labels_councillors = kmeans_councillors.labels_

agglomerative_model = AgglomerativeClustering(n_clusters=NUM_CLUSTERS)
agglomerative_result = agglomerative_model.fit_predict(councillors_vectors)


def get_details_by_cname(name):
    with open("councillor_details.json", "r") as file:
        json_data = json.load(file)
        return json_data[name]


parties_by_person = []
for index, person in enumerate(councillor_names):
    party = get_details_by_cname(person)["party"]
    parties_by_person.append(party)

df = pd.DataFrame({
    'Label': agglomerative_result,
    'Name': councillor_names,
    'Party': parties_by_person
})

fig, (ax0, ax1, ax2) = plt.subplots(nrows=1, ncols=3, figsize=(15, 10))

color_list = list(mcolors.TABLEAU_COLORS.keys())

label_colors = {}
for i in set(labels_councillors):
    label_colors[i] = color_list[i]

handles_0 = []
for i in unique(agglomerative_result):
    df_query = df.query("Label == @i")
    for index, row in df_query.iterrows():
        h = ax0.scatter(reduced_councillor_vectors[index][0], reduced_councillor_vectors[index][1], label=i,
                        c=label_colors[i])
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
        h = ax1.scatter(reduced_councillor_vectors[index][0], reduced_councillor_vectors[index][1], label=party,
                        c=label_colors[i])
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

for idx, cv in enumerate(councillors_vectors):
    pred = kmeans_councillors.predict(cv.reshape(1, -1))
    if pred[0] in cluster_councillor_map.keys():
        cluster_councillor_map[pred[0]].append(get_details_by_cname(councillor_names[idx])["party"])
    else:
        cluster_councillor_map[pred[0]] = [get_details_by_cname(councillor_names[idx])["party"]]

ic(cluster_councillor_map)

df_percentage = pd.DataFrame(columns=interested_parties)

for key in sorted(list(cluster_councillor_map.keys())):
    percentages = []
    for value in interested_parties:
        count = cluster_councillor_map[key].count(value)
        percentages.append(count / len(cluster_councillor_map[key]) * 100)
    df_percentage.loc[key] = percentages

ic(df_percentage)
