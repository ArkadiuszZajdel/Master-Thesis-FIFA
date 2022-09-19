from core.preprocessing.load_data import load_basic_df, select_date, load_df_with_shootouts
from core.preprocessing.conditions import add_conditions93, tournament, add_conditions06, set_simulation_years06, add_conditions_current

import pandas as pd
from datetime import date
from toolz import thread_first
from typing import Tuple, List


def pipeline_fifa93_98(start_year: int) -> pd.DataFrame:
    return thread_first(
            load_basic_df(),
            (select_date, date(start_year, 1, 1)),
            (add_conditions93, [3, 1, 0])
        )

def pipeline_fifa06_18(start_year: int, finish_year: int) -> Tuple[pd.DataFrame, List[date]]:
    return thread_first(
            load_df_with_shootouts(),
            (tournament, 1, 2, 2.5, 3, 4, 2),
            (select_date, date(start_year, 1, 1)),
            (add_conditions06, [3, 2, 1, 0])
        ), set_simulation_years06(start_year, finish_year)

def pipeline_fifa_current(start_year: int) -> pd.DataFrame:
    return thread_first(
            load_df_with_shootouts(),
            (tournament, 10, 20, 25, 40, 50, 15),
            (select_date, date(start_year, 1, 1)),
            (add_conditions_current, [1, 0.75, 0.5, 0])
    )