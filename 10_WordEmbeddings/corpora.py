from datetime import datetime
import spacy
import treetaggerwrapper
from spacy.lang.de.stop_words import STOP_WORDS

model = spacy.load("de_dep_news_trf")
import de_dep_news_trf


class Affair:

    def __init__(self, spp_business_obj, person_details, transcripts):
        self.spp_business_obj = spp_business_obj
        self.person_details = person_details
        self.transcripts = transcripts
        self.text_raw = {"InitialSituation": spp_business_obj["InitialSituation"],
                         "DraftText": spp_business_obj["DraftText"],
                         "ReasonText": spp_business_obj["ReasonText"],
                         "DocumentationText": spp_business_obj["DocumentationText"],
                         "MotionText": spp_business_obj["MotionText"],
                         "FederalCouncilResponseText": spp_business_obj["FederalCouncilResponseText"],
                         "FederalCouncilProposalText": spp_business_obj["FederalCouncilProposalText"]
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
                no_punct = [token for token in doc if not
                            token.is_punct and not token.is_digit and not token.is_currency and not token.is_bracket]
                for token in no_punct:
                    try:
                        text.join(f"{token.text.lower()} ")
                    except TypeError:
                        text.join(f"{token.text} ")
        self.text_clean = text

    def tag_text(self, **kwargs):
        text_to_tag = self.text_clean
        tagger = treetaggerwrapper.TreeTagger(**kwargs)
        tags = tagger.tag_text(text_to_tag)
        for idx, tag in enumerate(tags):
            text = tag.values()
            for token in text:
                if token.is_punct or token.is_digit or token.is_bracket or token.is_currency or token.is_quote or token.is_stop or token.text in STOP_WORDS:
                    tags.pop(idx)
                elif "+" in token.text or "@" in token.text:
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

    def get_affairs_by_person(self, last_name, first_name):
        try:
            return [affair for affair in self.values() if first_name == affair.spp_person_oj["FirstName"]
                    and last_name == affair.spp_person_oj["LastName"]]
        except KeyError:
            return "No such person"

    def get_affair_by_party(self, party):
        try:
            result = [affair for affair in self.values() if affair.person_details['party'] == party]
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
