import pandas as pd
from datetime import date

def load_basic_df() -> pd.DataFrame:
    df = pd.read_csv("loading/results.csv")
    return df.dropna()

def load_shootouts() -> pd.DataFrame:
    df = pd.read_csv("loading/shootouts.csv")
    return df.dropna()

def load_df_with_shootouts() -> pd.DataFrame:
    df_basic = load_basic_df()
    df_penalty = load_shootouts()
    return pd.merge(left=df_basic, right=df_penalty, how='left', left_on=['date', 'home_team', 'away_team'], right_on=['date', 'home_team', 'away_team'])

def select_date(df: pd.DataFrame, date: date) -> pd.DataFrame:
    return df[df['date']>=str(date)] #check types