import json
from icecream import ic
import gensim
from gensim.models import Doc2Vec
from tqdm import tqdm
import logging
import datetime
import os
from utils import interested_parties
from utils import get_numbers

user = os.environ["HOMEPATH"]

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

party_indices = {}
training_data = []
test_data = {}

num_tokens_by_party = get_numbers()[1]

for np in num_tokens_by_party:
    num_tokens_by_party[np] = num_tokens_by_party[np] * 0.95

file = open(rf"C:{user}\OneDrive - P.ARC AG\data.json", 'r', encoding='utf-8')
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
                    doc = gensim.models.doc2vec.TaggedDocument(tokens, [party])
                    if num_tokens_by_party[party] > 0:
                        training_data.append(doc)
                        num_tokens_by_party[party] -= len(tokens)
                    else:
                        test_data[affair_num] = doc

model = Doc2Vec(vector_size=100, min_count=2, epochs=50, window=4, hs=0, negative=1)
model.build_vocab(training_data)
model.train(training_data, total_examples=model.corpus_count, epochs=model.epochs)
model.save("DocModels\\tag_party.d2v")

file.close()
with open("test_data.json", encoding="utf-8", mode="w") as test_file:
    json.dump(test_data, test_file, ensure_ascii=False, indent=2)
