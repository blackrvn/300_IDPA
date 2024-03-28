from icecream import ic
from utils import get_details_by_cname
from utils import interested_parties

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from gensim.models import Doc2Vec
from sklearn.metrics.pairwise import cosine_similarity

import json

model = Doc2Vec.load(r"DocModels/tag_councillor.d2v")

councillor_vectors = model.dv.vectors
councillor_labels = model.dv.index_to_key

parties = [get_details_by_cname(c)["party"] for c in councillor_labels]

sp = [v for i, v in enumerate(councillor_vectors) if parties[i] == "SP"]
svp = [v for i, v in enumerate(councillor_vectors) if parties[i] == "SVP"]
fdp = [v for i, v in enumerate(councillor_vectors) if parties[i] == "FDP-Liberale"]
gruene = [v for i, v in enumerate(councillor_vectors) if parties[i] == "GRÜNE"]

sp_centroid = KMeans(n_clusters=1, random_state=0).fit(sp).cluster_centers_
svp_centroid = KMeans(n_clusters=1, random_state=0).fit(svp).cluster_centers_
fdp_centroid = KMeans(n_clusters=1, random_state=0).fit(fdp).cluster_centers_
gruene_centroid = KMeans(n_clusters=1, random_state=0).fit(gruene).cluster_centers_

centroids = [sp_centroid, svp_centroid, fdp_centroid, gruene_centroid]

sims = {"SP":
            {
                "SVP": cosine_similarity(sp_centroid, svp_centroid)[0][0],
                "FDP": cosine_similarity(sp_centroid, fdp_centroid)[0][0],
                "GRÜNE": cosine_similarity(sp_centroid, gruene_centroid)[0][0]
            }
        }
ic(sims)


