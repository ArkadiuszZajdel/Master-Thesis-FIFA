import pandas as pd
import numpy as np
from typing import Tuple
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV, RepeatedKFold, train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline

from resources.config import PREDICTION_PARAMS


def make_train_df(df: pd.DataFrame, train_size: int = 16000, test_size: int = 4000) -> pd.DataFrame:
    return df.tail(train_size + test_size).head(train_size) #each have to have we home away

def prepare_dfs_nonneutral(df_train: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df_home = df_train.loc[df_train.neutral == False].copy()
    df_home.We_home = round(df_home.We_home, 2)

    df_home_nonneutral = df_home[['We_home','home_score']].sort_values(by=['We_home']).groupby(['We_home']).mean()
    df_away_nonneutral = df_home[['We_home','away_score']].sort_values(by=['We_home']).groupby(['We_home']).mean() #we_home because we estimate everything based on we_home

    return df_home_nonneutral, df_away_nonneutral

def prepare_df_neutral(df_train: pd.DataFrame) -> pd.DataFrame:
    df_neutral1 = df_train.loc[df_train.neutral == True].copy()
    df_neutral2 = df_neutral1.copy()
    df_neutral2 = df_neutral2.drop(columns = ['We_home','home_score'])
    df_neutral2 = df_neutral2.rename(columns={'We_away': 'We_home', 'away_score': 'home_score'}) #create "away" in neutral same as "home" in neutral

    df_neutral = pd.concat([df_neutral1[['We_home','home_score']], df_neutral2[['We_home','home_score']]])
    df_neutral.We_home = round(df_neutral.We_home, 2)

    return df_neutral.sort_values(by=['We_home']).groupby(['We_home']).mean()


class Approximations:
    def __init__(self, df_home_nonneutral: pd.DataFrame, df_away_nonneutral: pd.DataFrame, df_neutral: pd.DataFrame): #df is after estimation and preprocessing
        self.df_home_nonneutral = df_home_nonneutral
        self.df_away_nonneutral = df_away_nonneutral
        self.df_neutral = df_neutral

        cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
        pipeline = Pipeline(
            [
                ('scaler', StandardScaler()),
                ('model', Ridge())
            ]
        )

        self.find_optimal_model = GridSearchCV(
            pipeline,
            {'model__alpha': np.arange(0.1,10,0.1)},
            cv = cv,
            scoring = "neg_mean_squared_error",
            verbose = 3,
            n_jobs=-1
        )

    def approximate_home_regression(self):
        we_home = self.df_home_nonneutral[self.df_home_nonneutral.index.values<PREDICTION_PARAMS["THRESHOLD_HOME"]].index.values.reshape(-1,1)
        goals_home = self.df_home_nonneutral[self.df_home_nonneutral.index.values<PREDICTION_PARAMS["THRESHOLD_HOME"]].home_score.values.reshape(-1,1)

        polynomial = PolynomialFeatures(PREDICTION_PARAMS["POLYNOMIAL_REGRESSION_DEGREE_HOME"], include_bias = False)
        transformed_polynomial = polynomial.fit_transform(we_home)

        X_train, _, y_train, _ = train_test_split(transformed_polynomial, goals_home, test_size=0.3, random_state=43) #maybe useless

        results_split = self.find_optimal_model.fit(X_train, y_train)
        return results_split.best_estimator_