import numpy as np
import pandas as pd
from typing import List

def add_conditions(df: pd.DataFrame, points: List[int]) -> pd.DataFrame:
    df.loc[:,"diff"] = df["home_score"] - df["away_score"]

    conditions = set_conditions(df)

    values1 = points.copy() #[3,1,0]
    points.reverse()
    values2 = points #[0,1,3]
    values = [1,0.5,0] #############pracowac
    df.loc[:,"W_home"] = np.select(conditions, values1)
    df.loc[:,"W_away"] = np.select(conditions, values2)
    df.loc[:,"W"] = np.select(conditions, values)
    return df

def set_conditions(df: pd.DataFrame) -> list:
    return [
        (df["diff"] > 0),
        (df["diff"] == 0),
        (df["diff"] < 0)
        ]

def find_unique_countries(df: pd.DataFrame) -> List[str]:
    unique1 = pd.unique(df["home_team"])
    unique2 = pd.unique(df["away_team"])
    return np.unique(np.concatenate((unique1,unique2),0))