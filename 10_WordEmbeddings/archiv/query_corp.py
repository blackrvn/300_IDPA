import pickle
from icecream import ic
from corpora import *

corpus = pickle.load(open('corpora.pickle', 'rb'))
ic(corpus.get_affairs_by_person("Bregy Philipp Matthias")[0].clean_text())
ic(corpus.get_affairs_by_person("Bregy Philipp Matthias")[0].tag_text(TAGPARFILE='german.par',
                                                                      TAGABBREV='german-abbreviations'))
ic(corpus.get_affairs_by_person("Bregy Philipp Matthias")[0].text_tagged)

