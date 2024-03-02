import gensim


class Document:
    def __init__(self, name, tagged_doc: gensim.models.doc2vec.TaggedDocument):
        self.name = name
        self.doc_vector = None
        self.tagged_doc = tagged_doc
        self.words = self.tagged_doc.words
        self.similarities = []

    def get_most_similar_doc(self):
        return self.similarities[0]["Document"]

    def get_similarities(self):
        return self.similarities

    def get_least_similar_doc(self):
        return self.similarities[-1]["Document"]

    def set_doc_vector(self, vector):
        self.doc_vector = vector


