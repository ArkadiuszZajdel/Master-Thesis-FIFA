import numpy as np
import pandas as pd
from typing import List, Dict
from core.preprocessing.enums import Ranking

#fifa93
def add_conditions93(df: pd.DataFrame, points: List[int]) -> pd.DataFrame:
    df.loc[:,"diff"] = df["home_score"] - df["away_score"]

    conditions = _set_conditions93(df)

    values1 = points.copy() # for example [3,1,0]
    points.reverse()
    values2 = points #[0,1,3]
    values = [1,0.5,0]

    df.loc[:,"W_home"] = np.select(conditions, values1)
    df.loc[:,"W_away"] = np.select(conditions, values2)
    df.loc[:,"W"] = np.select(conditions, values)
    return df.copy()

def _set_conditions93(df: pd.DataFrame) -> List[pd.Series]:
    return [
        (df["diff"] > 0),
        (df["diff"] == 0),
        (df["diff"] < 0)
        ]


#fifa06
def add_conditions06(df: pd.DataFrame, points: List[int]) -> pd.DataFrame:
    df.loc[:,"diff"] = df["home_score"] - df["away_score"]

    conditions = _set_conditions06(df)
    values1 = points.copy() # for example [3,2,1,0]
    points.reverse()
    values2 = points #[0,1,2,3]
    df.loc[:,list(conditions.keys())[0]] = np.select(list(conditions.values())[0], values1)
    df.loc[:,list(conditions.keys())[1]] = np.select(list(conditions.values())[1], values2)

    conditions = _set_conditions_real_scores06(df)
    values = [1,0.5,0]
    df.loc[:,list(conditions.keys())[0]] = np.select(list(conditions.values())[0], values)
    df.loc[:,list(conditions.keys())[1]] = np.select(list(conditions.values())[1], values)
    return df.copy()

def _set_conditions06(df: pd.DataFrame) -> Dict[str,List[pd.Series]]:
    return {
        'W_home': [
            (df["diff"] > 0),
            (df["home_team"] == df["winner"]),
            ((df["diff"] == 0) & (df["winner"]!=df["home_team"])),
            (df["diff"] < 0)
        ],
        'W_away': [
            (df["diff"] > 0),
            ((df["diff"] == 0) & (df["winner"] != df["away_team"])),
            (df["away_team"] == df["winner"]),
            (df["diff"] < 0)
        ]
    }

def _set_conditions_real_scores06(df: pd.DataFrame) -> Dict[str,List[pd.Series]]:
    return {
        'W_home_real': [(df["W_home"] > 1), (df["W_home"] == 1), (df["W_home"] < 1)],
        'W_away_real': [(df["W_away"] > 1), (df["W_away"] == 1), (df["W_away"] < 1)]
    }

def set_simulation_years06(start_year: int, finish_year: int) -> List[str]:
    return [str(year+1)+'-01-01' for year in range(start_year+1, finish_year+1)]


#fifa current
def add_conditions_current(df: pd.DataFrame, points: List[float]) -> pd.DataFrame:
    df.loc[:,"diff"] = df["home_score"] - df["away_score"]

    conditions = _set_conditions_current(df)
    values1 = points.copy() # for example [1,0.75,0.5,0]
    points.reverse()
    values2 = points #[0,0.5,0.75,1]
    df.loc[:,list(conditions.keys())[0]] = np.select(list(conditions.values())[0], values1)
    df.loc[:,list(conditions.keys())[1]] = np.select(list(conditions.values())[1], values2)

    return df.copy()

def _set_conditions_current(df: pd.DataFrame) -> Dict[str,List[pd.Series]]:
    return {
        'W_home': [
            (df["diff"] > 0),
            (df["home_team"] == df["winner"]),
            ((df["diff"] == 0) & (df["winner"] != df["home_team"])),
            (df["diff"] < 0)
        ],
        'W_away': [
            (df["diff"] > 0),
            ((df["diff"] == 0) & (df["winner"] != df["away_team"])),
            (df["away_team"] == df["winner"]),
            (df["diff"] < 0)
        ]
    }


def find_unique_countries(df: pd.DataFrame) -> List[str]:
    unique1 = pd.unique(df["home_team"])
    unique2 = pd.unique(df["away_team"])
    return np.unique(np.concatenate((unique1,unique2),0))


def tournament(df: pd.DataFrame, friendly: float, nl: float, quali: float, continental: float,
worldcup: float, other: float) -> pd.DataFrame:
    df["tournament_parameter"] = df.apply(lambda row: _add_tournament_parameter(row.tournament, friendly, nl, quali, continental, worldcup, other), axis = 1)
    return df

def _add_tournament_parameter(row_tournament: str, friendly: float, nl: float,
quali: float, continental: float, worldcup: float, other: float) -> float:
    if row_tournament == "Friendly":
        return friendly
    elif "Nations League" in row_tournament and "qualification" not in row_tournament:
        return nl
    elif row_tournament in ["FIFA World Cup qualification", "AFC Asian Cup qualification",
    "UEFA Euro qualification", "African Cup of Nations qualification",
    "Gold Cup qualification", "Copa América qualification"]:
        return quali
    elif row_tournament in ["AFC Asian Cup", "UEFA Euro", "African Cup of Nations", "Gold Cup", "Copa América"]:
        return continental
    elif row_tournament == "FIFA World Cup":
        return worldcup
    else:
        return other