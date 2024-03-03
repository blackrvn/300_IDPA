from datetime import datetime
import json


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
        self.text_cleaned = None


class Corpora(dict):
    def __init__(self):
        super().__init__()

    def get_all_affairs(self):
        return self.values()

    def get_affairs_by_time_period(self, start_date: datetime, end_date: datetime):
        return [affair for affair in self.values() if
                start_date <= affair.spp_business_obj["SubmissionDate"] <= end_date]

    def get_affairs_by_person(self, last_name, first_name):
        return [affair for affair in self.values() if first_name == affair.spp_person_oj["FirstName"]
                and last_name == affair.spp_person_oj["LastName"]]

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
            text = []
            for value in affair.spp_business_obj.text_raw.values():
                if value is not None:
                    text.append(value)
            texts[affair.spp_business_obj["ID"]] = text
        return texts

    def get_affair_by_id(self, affair_id):
        return self["affair_id"]
