def calculate_elo_probability(ranking_home: float, ranking_away: float,
neutral: bool, importance: int, sensitivity: int, home_buff: int) -> float:       
    if(neutral == False):
        return 1/(1+importance**(-(ranking_home-ranking_away+home_buff)/sensitivity))
    else:
        return 1/(1+importance**(-(ranking_home-ranking_away)/sensitivity))