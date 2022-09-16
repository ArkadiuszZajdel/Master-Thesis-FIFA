import pandas as pd
from datetime import date
import pickle
from core.preprocessing.conditions import find_unique_countries

def load_basic_df() -> pd.DataFrame:
    df = pd.read_csv("resources/results.csv")
    return df.dropna()

def load_shootouts() -> pd.DataFrame:
    df = pd.read_csv("resources/shootouts.csv")
    return df.dropna()

def load_df_with_shootouts() -> pd.DataFrame:
    df_basic = load_basic_df()
    df_penalty = load_shootouts()
    return pd.merge(left=df_basic, right=df_penalty, how='left', left_on=['date', 'home_team', 'away_team'], right_on=['date', 'home_team', 'away_team'])

def select_date(df: pd.DataFrame, date: date) -> pd.DataFrame:
    return df.loc[df['date']>=str(date)].copy()

def load_and_set_confederation(df: pd.DataFrame) -> pd.DataFrame:
    try:
        confs = pickle.load(open("resources/confederation.pickle", "rb"))
    except FileNotFoundError:
        asia=pd.read_html("https://en.wikipedia.org/wiki/Asian_Football_Confederation")
        asia=asia[4].Name
        america=pd.read_html("https://en.wikipedia.org/wiki/CONCACAF")
        america=america[3].Association
        samerica=pd.read_html("https://en.wikipedia.org/wiki/CONMEBOL")
        samerica=samerica[4].Association
        oceania=pd.read_html("https://en.wikipedia.org/wiki/Oceania_Football_Confederation")
        oceania=oceania[3].Association
        europa=pd.read_html("https://en.wikipedia.org/wiki/UEFA")
        europa=europa[3].Association

        america=america.drop([3,11])
        america=america["North American Zone (NAFU) (3)"].str.split("[",expand=True).drop(columns=[1])
        america["c"]=0.85
        america.set_index(0,inplace=True)

        asia=asia.drop([12,19,30,38])
        asia=asia["ASEAN Football Federation (AFF) (12)"].str.split("[",expand=True).drop(columns=[1])
        asia["c"]=0.85
        asia.set_index(0,inplace=True)

        oceania=pd.DataFrame({"0":oceania.to_numpy(),"c":0.85})
        oceania.set_index("0",inplace=True)

        samerica=pd.DataFrame({"0":samerica.to_numpy(),"c":1})
        samerica.set_index("0",inplace=True)

        europa=pd.DataFrame({"0":europa.to_numpy()})
        europa=europa["0"].str.split("[",expand=True).drop(columns=[1])
        europa.set_index(0,inplace=True)
        europa["c"]=1

        unique_countries = find_unique_countries(df)

        confs=pd.concat([asia,america,samerica,europa,oceania])

        africa=pd.DataFrame({"Country":list(set(unique_countries)-set(confs.index.to_numpy())),"c":0.9})
        africa=africa.set_index("Country")

        confs=pd.concat([confs,africa])
        pickle.dump(confs, open("resources/confederation.pickle", "wb"))
    return confs