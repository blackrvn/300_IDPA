import swissparlpy as spp
import pandas as pd
from datetime import datetime
from datetime import timezone
from datetime import date
import numpy as np


def get_spp_data(start_date, end_date):
    bs = spp.get_data(
        "Business",
        Language="DE",
        SubmissionDate=datetime.fromisoformat("2023-12-21 00:00:00+00:00"))
    return bs


lst = []

for date in range(2010, 2024):
    start = f"{date}-01-01 00:00:00+00:00"
    end = f"{date + 1}-01-01 00:00:00+00:00"
    business = get_spp_data(start, end)
    lst.append(pd.DataFrame(business))

print(lst)
