from datetime import datetime
import spacy
import treetaggerwrapper
from spacy.lang.de.stop_words import STOP_WORDS
from icecream import ic

model = spacy.load("de_dep_news_trf")
import de_dep_news_trf


class Affair:

    def __init__(self, spp_business_obj, person_details, transcripts):
        self.spp_business_obj = spp_business_obj
        self.person_details = person_details
        self.transcripts = transcripts
        self.text_raw = {"InitialSituation": spp_business_obj["InitialSituation"],
                         "Title": spp_business_obj["Title"],
                         "DraftText": spp_business_obj["DraftText"],
                         "ReasonText": spp_business_obj["ReasonText"],
                         "DocumentationText": spp_business_obj["DocumentationText"],
                         "MotionText": spp_business_obj["MotionText"]
                         }
        self.text_clean = None
        self.text_tagged = None

    def clean_text(self):
        text_raw = self.get_raw_text()
        text = ''
        for string in text_raw.values():

            if isinstance(string, str):
                nlp = de_dep_news_trf.load()
                doc = nlp(string)
                clean = [token for token in doc if not
                         token.is_punct and not token.is_digit and not token.is_currency
                         and not token.is_bracket and len(token.text) > 1]
                for token in clean:
                    text += token.text.lower().strip('<p>').strip('</p>') + " "
        self.text_clean = text

    def tag_text(self, **kwargs):
        text_to_tag = self.text_clean
        tagger = treetaggerwrapper.TreeTagger(**kwargs)
        tags = treetaggerwrapper.make_tags(tagger.tag_text(text_to_tag))
        for idx, tag in enumerate(tags):
            lemma = tag[-1]
            ic(lemma)
            if lemma in STOP_WORDS:
                tags.pop(idx)
            elif "+" in lemma or "@" in lemma:
                tags.pop(idx)

        self.text_tagged = tags

    def get_raw_text(self):
        return self.text_raw

    def get_clean_text(self):
        return self.text_clean

    def get_tagged_text(self):
        return self.text_tagged

    def get_lemma(self):
        return [tag["Lemma"] for tag in self.text_tagged]


class Corpora(dict):
    def __init__(self):
        super().__init__()

    def get_all_affairs(self):
        return self.values()

    def get_affairs_by_time_period(self, start_date: datetime, end_date: datetime):
        return [affair for affair in self.values() if
                start_date <= affair.spp_business_obj["SubmissionDate"] <= end_date]

    def get_affairs_by_person(self, name):
        try:
            result = []
            for affair in self.values():
                if isinstance(affair.person_details, dict):
                    if affair.spp_business_obj["SubmittedBy"] == name:
                        result.append(affair)
            return result
        except KeyError:
            return "No such person"

    def get_affair_by_party(self, party):
        try:
            result = []
            for affair in self.values():
                if isinstance(affair.person_details, dict):
                    if 'party' in affair.person_details.keys():
                        if affair.person_details["party"] == party:
                            result.append(affair)
                else:
                    pass
            if len(result) > 0:
                return result
            else:
                return "No such party"
        except KeyError:
            return "No such key"

    def get_person_details(self):
        return [affair.person_details for affair in self.values()]

    def get_text(self, affair_objs=None):
        if not affair_objs:
            affair_objs = self.get_all_affairs()
        texts = {}
        for affair in affair_objs:
            text = ''
            for value in affair.text_raw.values():
                if value is not None:
                    text.join(f"{value} ")
            texts[affair.spp_business_obj["ID"]] = text
        return texts

    def get_affair_by_id(self, affair_id):
        return self[affair_id]
