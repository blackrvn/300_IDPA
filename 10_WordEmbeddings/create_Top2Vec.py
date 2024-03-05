import gensim
import os
import glob
from utils import Document
from top2vec import Top2Vec

doc_path = r'..\09_Quellen\Parteiprogramme\tagged'
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
common_text = [doc.words for doc in docs]
print(common_text[0])
sp_corp = []
svp_corp = []
for doc in docs:
    print(doc.name)
    if 'SP' in doc.name:
        for w in doc.words:
            sp_corp.append(w)
    else:
        for w in doc.words:
            svp_corp.append(w)

print(sp_corp)
model = Top2Vec(svp_corp, speed='learn', workers=8, min_count=10)
model.hierarchical_topic_reduction(num_topics=10)
topic_words, word_scores, topic_scores, topic_nums = model.search_topics(keywords=["ausland"], num_topics=5)
print(topic_words)
for topic in topic_nums:
    model.generate_topic_wordcloud(topic)
