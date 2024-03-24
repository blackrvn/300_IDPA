from gensim.models import Doc2Vec
from icecream import ic

from query_json import interested_parties

ic(interested_parties)

populist_words = ["eliten", "politiker", "establishment", "wahrheit", "verrat", "skandal"]

for party in interested_parties[1:2]:
    model = Doc2Vec.load(rf'DocModels\tag_{party}.d2v')
    word_vectors = model.wv
    test_vectors = [model.infer_vector([word]) for word in populist_words]
    for i, word in enumerate(populist_words):
        sim = model.wv.most_similar(test_vectors[i], topn=5)
        ic(f"{word}: {sim}")

