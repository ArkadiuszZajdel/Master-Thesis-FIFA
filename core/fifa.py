import pandas as pd
from typing import Dict, Tuple

from core.preprocessing import find_unique_countries
from core.elo import calculate_elo_probability_and_update_ranking

def estimate93(df: pd.DataFrame, importance: int, sensitivity: int, home_buff: int) -> Tuple[pd.DataFrame, Dict[str, int]]:
    unique_countries = find_unique_countries(df)
    
    ranking = {country:0 for country in unique_countries}

    #czy moge po kropce
    df['We_home'] = df.apply(lambda row: calculate_elo_probability_and_update_ranking(row.home_team, row.W_home, row.away_team, row.W_away, row.neutral, ranking, importance, sensitivity, home_buff), axis = 1)
    df["W-We_home"] = df["W"]-df["We_home"]
    return df, ranking