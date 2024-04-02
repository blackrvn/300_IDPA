import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import unique
import gensim
from gensim.models import Doc2Vec
from icecream import ic
from sklearn.manifold import TSNE
from utils import get_details_by_cname
from utils import interested_parties
from utils import calculate_accuracy
from utils import get_num_councillors
from utils import clean_text, tag_text

model = Doc2Vec.load(r'DocModels\tag_party.d2v')
party_vectors = np.array([model.dv[p] for p in interested_parties])

s1 = "Das Volk muss sich gegen die korrupten Eliten erheben und für die wahre Freiheit kämpfen."
s2 = "Die politische Klasse verrät das Volk, indem sie sich den Interessen der Banker und Geschäftsleute unterwirft."
s3 = "Wir, das Volk, müssen die Wahrheit über die Machenschaften der politischen Propaganda aufdecken."

statements = [s1, s2, s3]
labels = []
docs = []

for i, s in enumerate(statements):
    labels.append(f"s{i+1}")
    cleaned_text = clean_text(s)
    tagged_text = tag_text(cleaned_text)
    lemmas_text = " ".join(tagged_text["Lemmas"])
    tokens = gensim.utils.simple_preprocess(lemmas_text, max_len=100)
    doc = gensim.models.doc2vec.TaggedDocument(tokens, [f"s{i+1}"])
    docs.append(doc)

ic(docs)

sims = []

for d in docs:
    inferred_vector = model.infer_vector(d.words)
    most_similar = model.dv.cosine_similarities(inferred_vector, party_vectors)
    sims.append(most_similar)

sims = np.array(sims).reshape(len(statements), len(interested_parties)).transpose()
ic(sims)
party_colors = ["r", "c", "b", "y", "g", "orange"]

# Create bar chart with grouped bars and different colors
plt.figure(figsize=(10, 6))
bar_width = 0.15
x = np.arange(len(statements))

for i, similarities in enumerate(sims):
    plt.bar(x + i * bar_width, similarities, bar_width, label=interested_parties[i], color=party_colors[i])

plt.xlabel('Aussagen')
plt.ylabel('Ähnlichkeit zu Partei')
plt.xticks(x + bar_width * 2.5, labels=labels, rotation=45, ha='right')
plt.legend()
plt.tight_layout()
plt.savefig(r"C:\Users\lukas\Documents\300_IDPA\09_Quellen\Plots\Q2_PopStatements.png")
plt.show()

