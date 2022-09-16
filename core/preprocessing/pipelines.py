from core.preprocessing.load_data import load_basic_df, select_date, load_df_with_shootouts
from core.preprocessing.conditions import add_conditions93, tournament, add_conditions06

import pandas as pd
from datetime import date
from toolz import thread_first


def pipeline_fifa93_98() -> pd.DataFrame:
    return thread_first(
            load_basic_df(),
            (select_date, date(2000,1,1)),
            (add_conditions93, [3,1,0])
        )

def pipeline_fifa06_18() -> pd.DataFrame:
    return thread_first(
            load_df_with_shootouts(),
            (tournament, 1, 2, 2.5, 3, 4, 2),
            (select_date, date(2000,1,1)),
            (add_conditions06, [3,2,1,0])
        )