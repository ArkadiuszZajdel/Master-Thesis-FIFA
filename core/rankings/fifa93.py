import pandas as pd
from typing import Dict, Tuple

from core.preprocessing import find_unique_countries
from core.rankings.elo import calculate_elo_probability

class FIFA93:
    def __init__(self, df: pd.DataFrame, importance: int, sensitivity: int, home_buff: int):
        self.df = df
        self.importance = importance
        self.sensitivity = sensitivity
        self.home_buff = home_buff

        self.unique_countries = find_unique_countries(df)
        self.ranking = {country:0 for country in self.unique_countries}

    def estimate93(self) -> Tuple[pd.DataFrame, Dict[str, int]]:
        self.df['We_home'] = self.df.apply(lambda row: self._calculate_elo_probability_and_update_ranking(row.home_team, row.W_home, row.away_team, row.W_away, row.neutral), axis = 1)
        self.df['We_away'] = 1 - self.df['We_home']
        self.df["W-We_home"] = self.df["W"] - self.df["We_home"] #nozliwe ze nie potrzebne bo to tylko do mse
        return self.df, self.ranking

    def _calculate_elo_probability_and_update_ranking(self, country_home: str, score_home: int, 
    country_away: str, score_away: int, neutral: bool) -> float:
        self.ranking[country_home] += score_home
        self.ranking[country_away] += score_away

        return calculate_elo_probability(self.ranking[country_home], self.ranking[country_away], neutral, self.importance, self.sensitivity, self.home_buff)