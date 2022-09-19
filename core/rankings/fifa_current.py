import pandas as pd
from typing import Dict, Tuple

from core.preprocessing import find_unique_countries
from core.rankings.elo import calculate_elo_probability

class FIFAcurrent:
    def __init__(self, df: pd.DataFrame, importance: int = 10, sensitivity: int = 600, home_buff: int = 0):
        self.df = df
        self.importance = importance
        self.sensitivity = sensitivity
        self.home_buff = home_buff

        self.unique_countries = find_unique_countries(df)
        self.ranking = {country: 1200 for country in self.unique_countries}

    def estimate_current_fifa(self) -> Tuple[pd.DataFrame, Dict[str, int]]:
        self.df['We_home'], self.df['We_away'] = zip(*self.df.apply(lambda row: self._update_after_match(row.home_team, row.away_team,
                                                        row.neutral, row.W_home, row.W_away, row.tournament_parameter), axis = 1))

        # df["W_home-We_home"] = df["W_home"]-df["We_home"]
        # df["W_away-We_away"] = df["W_away"]-df["We_away"]
        # df_1loop = df.copy()                 only for ranking comparison
        # ranking_1loop = ranking.copy()
        
        #second loop with new starting ranking
        self.df['We_home'], self.df['We_away'] = zip(*self.df.apply(lambda row: self._update_after_match(row.home_team, row.away_team,
                                                        row.neutral, row.W_home, row.W_away, row.tournament_parameter), axis = 1))

        self.df["W_home-We_home"] = self.df["W_home"]-self.df["We_home"] #only for mse
        self.df["W_away-We_away"] = self.df["W_away"]-self.df["We_away"] #same

        return self.df, self.ranking

    def _update_after_match(self, home_team: str, away_team: str, neutral: bool, home_score: int, away_score: int, tournament_parameter: float) -> Tuple[float, float]:
        ranking_home = self.ranking[home_team]
        ranking_away = self.ranking[away_team]

        we_home = calculate_elo_probability(ranking_home, ranking_away, neutral, self.importance, self.sensitivity, self.home_buff)
        
        self.ranking[home_team] += int(tournament_parameter * (home_score - we_home))
        self.ranking[away_team] += int(tournament_parameter * (away_score - (1 - we_home)))

        return we_home, 1 - we_home