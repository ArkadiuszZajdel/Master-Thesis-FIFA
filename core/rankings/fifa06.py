import pandas as pd
import numpy as np
from typing import Dict, Tuple, List

from core.preprocessing import find_unique_countries, load_and_set_confederation
from core.rankings.elo import calculate_elo_probability

class FIFA06:
    def __init__(self, df: pd.DataFrame, importance: int, sensitivity: int, home_buff: int, simulation_years: List[str]):
        self.df = df
        self.importance = importance
        self.sensitivity = sensitivity
        self.home_buff = home_buff
        self.simulation_years = simulation_years

        self.unique_countries = find_unique_countries(df)
        self.confs = load_and_set_confederation(df)

        self.year_indicator: int = 0
        self.places: List[int] = []
        self.ranking: pd.DataFrame = pd.DataFrame()


    def estimate06(self) -> Tuple[pd.DataFrame, Dict[str, float]]:        
        self._create_ranking_components06()
        self._create_places_interpreter06()
               
        self.df['We_home'], self.df['We_away'] = zip(*self.df.apply(lambda row: self._update_after_match06(row.date,
                    row.home_team, row.away_team, row.neutral, row.W_home, row.W_away, row.tournament_parameter), axis = 1))
        self.df["W_home_real-We_home"] = self.df["W_home_real"] - self.df["We_home"] #only for mse
        self.df["W_away_real-We_away"] = self.df["W_away_real"] - self.df["We_away"] #same
        
        ranking_dict = dict(zip(self.ranking.index, self.ranking.overall))
        return(self.df, ranking_dict)

    def _create_ranking_components06(self) -> None:
        self.ranking = pd.DataFrame({'country': self.unique_countries, 
                            'nr_of_games_in_year': 0,
                            '1': 0, '0.5': 0, '0.3': 0, '0.2': 0, #years score rankings (column name is multiplier of given year)
                            'overall': 0, 'place': 0})
        self.ranking = self.ranking.set_index('country')

    def _create_places_interpreter06(self) -> None:
        self.places = [2]
        self.places.extend(range(2,151))
        self.places.extend([150]*(len(self.unique_countries)-150))
            
    def _update_after_match06(self, date: str, home_team: str, away_team: str, neutral: bool,
    home_score: int, away_score: int, tournament_parameter: float) -> Tuple[float, float]:
        if date > self.simulation_years[self.year_indicator]:
            self._update_ranking_components_after_year06()
            self.year_indicator += 1

        rank_home = self.ranking.loc[home_team, 'overall']
        rank_away = self.ranking.loc[away_team, 'overall']

        we_home = calculate_elo_probability(rank_home, rank_away, neutral, self.importance, self.sensitivity, self.home_buff)

        self._update_ranking_components_after_match06(self.simulation_years[self.year_indicator], self.simulation_years[0],
                home_team, home_score, away_team, away_score, tournament_parameter)

        return we_home, 1 - we_home

    def _update_ranking_components_after_year06(self) -> None:
        self.ranking['1'] = self.ranking['1'].divide(self.ranking['nr_of_games_in_year']).replace(np.inf, 0).replace(np.nan, 0)
        self.ranking['overall'] = self.ranking['1']+0.5*self.ranking['0.5']+0.3*self.ranking['0.3']+0.2*self.ranking['0.2']
        
        self.ranking['nr_of_games_in_year'] = 0
        self.ranking['0.2'], self.ranking['0.3'], self.ranking['0.5'], self.ranking['1']  = self.ranking['0.3'], self.ranking['0.5'], self.ranking['1'], 0
        
        self.ranking = self.ranking.sort_values('overall', ascending = False)
        self.ranking['place'] = self.places

    def _update_ranking_components_after_match06(self, actual_year: str, first_year: str,
    home_team: str, home_score: int, away_team: str, away_score: int,
    tournament_parameter: float) -> None:
        if actual_year >= first_year:
            self.ranking.loc[home_team, "1"] += home_score * tournament_parameter * (200-self.ranking.loc[away_team,'place']) * self.confs.loc[away_team,"c"]
            self.ranking.loc[home_team, "nr_of_games_in_year"] += 1

            self.ranking.loc[away_team, "1"] += away_score * tournament_parameter * (200-self.ranking.loc[home_team,'place']) * self.confs.loc[home_team,"c"]
            self.ranking.loc[away_team, "nr_of_games_in_year"] += 1
        else:
            self.ranking.loc[home_team, "1"] += home_score * tournament_parameter * 1/2 * self.confs.loc[away_team,"c"]
            self.ranking.loc[home_team, "nr_of_games_in_year"] += 1

            self.ranking.loc[away_team, "1"] += away_score * tournament_parameter * 1/2 * self.confs.loc[home_team,"c"]
            self.ranking.loc[away_team, "nr_of_games_in_year"] += 1