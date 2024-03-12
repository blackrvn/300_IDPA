import json
from icecream import ic
import gensim
from gensim.models import Doc2Vec
from tqdm import tqdm
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

file = open(r"C:\Users\lukas\Downloads\affairs.json", 'r', encoding='utf-8')
data = json.load(file)

party_indices = {}
corpus = []

for idx, affair in tqdm(enumerate(data), total=len(data)):
    if "councillor" in affair["author"].keys() and "party" in affair["author"]["councillor"].keys():
        party = affair["author"]["councillor"]["party"]
        councillor = affair["author"]["councillor"]["name"]
        for d in affair["texts"]:

            if "tagged" in d.keys():
                lemmas = d["tagged"]["Lemmas"]
                lemmas_text = " ".join(lemmas)
                tokens = gensim.utils.simple_preprocess(lemmas_text)
                doc = gensim.models.doc2vec.TaggedDocument(tokens, [idx, party, councillor])
                corpus.append(doc)


model = Doc2Vec(vector_size=70, min_count=5, epochs=50, window=5, hs=1)
model.build_vocab(corpus)
model.train(corpus, total_examples=model.corpus_count, epochs=model.epochs)
model.save("affairs.d2v")

"""
test_vec = model.infer_vector(test_doc)
ic(model.dv.most_similar(model.dv["SP"], topn=3))
"""

file.close()
