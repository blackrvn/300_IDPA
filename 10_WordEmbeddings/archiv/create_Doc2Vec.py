import gensim
from gensim.models import Doc2Vec
from gensim import corpora

import os
import glob
import pickle
from icecream import ic
from tqdm import tqdm
import pprint
import collections

from utils import Document

doc_path = r'../../09_Quellen/Parteiprogramme/tagged'
file_dirs = glob.glob(os.path.join(doc_path, '*.lem'))


def read_corpus():
    for idx, file in enumerate(file_dirs):
        fname = file.split('\\')[-1].strip('.lem')
        with open(file, 'r', encoding='utf-8') as f:
            doc = ''
            for line in f.readlines():
                text = line.strip("\n")
                doc += f'{text} '
            tokens = gensim.utils.simple_preprocess(doc)
            doc = Document(fname, gensim.models.doc2vec.TaggedDocument(tokens, [idx]))
            yield doc


docs = list(read_corpus())
train_corpus = [doc.tagged_doc for doc in docs]
model = Doc2Vec(vector_size=300, min_count=1, epochs=40)
model.build_vocab(train_corpus)
model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)

for idx, doc in enumerate(docs):
    doc.doc_vector = model.infer_vector(doc.words)
    sims = model.dv.most_similar([doc.doc_vector], topn=len(model.dv))
    for sim in sims:
        doc_obj = docs[sim[0]]
        doc.similarities.append({"Document": doc_obj, "Similarity": sim[1], "Document name": doc_obj.name})
    ic(doc.get_most_similar_doc().name)
    ic(doc.get_least_similar_doc().name)

