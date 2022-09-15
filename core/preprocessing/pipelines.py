from core.preprocessing.load_data import load_basic_df, select_date
from core.preprocessing.conditions import add_conditions

import pandas as pd
from datetime import date
from toolz import thread_first


def pipeline_fifa93_98() -> pd.DataFrame:
    return thread_first(load_basic_df(), (select_date, date(2000,1,1)), (add_conditions, [3,1,0]))