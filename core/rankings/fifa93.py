import pandas as pd
from typing import Dict, Tuple

from core.preprocessing import find_unique_countries
from core.rankings.elo import calculate_elo_probability

def estimate93(df: pd.DataFrame, importance: int, sensitivity: int, home_buff: int) -> Tuple[pd.DataFrame, Dict[str, int]]:
    unique_countries = find_unique_countries(df)
    
    ranking = {country:0 for country in unique_countries}

    df['We_home'] = df.apply(lambda row: _calculate_elo_probability_and_update_ranking(row.home_team, row.W_home, row.away_team, row.W_away, row.neutral, ranking, importance, sensitivity, home_buff), axis = 1)
    df["W-We_home"] = df["W"]-df["We_home"] #nozliwe ze nie potrzebne bo to tylko do mse
    return df, ranking

def _calculate_elo_probability_and_update_ranking(country_home: str, score_home: int, 
country_away: str, score_away: int,
neutral: bool, ranking: Dict[str, int],
importance: int, sensitivity: int, home_buff: int) -> float:
    ranking[country_home] += score_home
    ranking[country_away] += score_away

    return calculate_elo_probability(ranking[country_home], ranking[country_away], neutral, importance, sensitivity, home_buff)