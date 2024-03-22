import json
from icecream import ic
import gensim
from gensim.models import Doc2Vec
from tqdm import tqdm
import logging
import datetime

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

interested_parties = ["SP", "SVP", "FDP-Liberale", "glp", "GRÜNE", "M-E"]

party_indices = {}
corpus = []

if __name__ == "__main__":
    file = open(r"C:\Users\vruser01\OneDrive - P.ARC AG\test.json", 'r', encoding='utf-8')
    data = json.load(file)
    for affair in tqdm(data, total=len(data)):
        if ("councillor" in affair["author"].keys()
                and "party" in affair["author"]["councillor"].keys()
                and datetime.datetime.fromisoformat(affair["deposit"]["date"][:10]).year > 1969):
            party = affair["author"]["councillor"]["party"]
            if party in interested_parties:
                councillor = affair["author"]["councillor"]["name"]
                affair_num = affair["shortId"]
                for d in affair["texts"]:

                    if "tagged" in d.keys():
                        lemmas = d["tagged"]["Lemmas"]
                        lemmas_text = " ".join(lemmas)
                        tokens = gensim.utils.simple_preprocess(lemmas_text)
                        doc = gensim.models.doc2vec.TaggedDocument(tokens, [affair_num])
                        corpus.append(doc)

    model = Doc2Vec(vector_size=70, min_count=1, epochs=100, window=5, hs=1)
    model.build_vocab(corpus)
    model.train(corpus, total_examples=model.corpus_count, epochs=model.epochs)
    model.save("DocModels\\tag_shortid_1970.d2v")

    """
    test_vec = model.infer_vector(test_doc)
    ic(model.dv.most_similar(model.dv["SP"], topn=3))
    """

    file.close()
