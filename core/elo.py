from typing import Dict

def calculate_elo_probability_and_update_ranking(country_home: str, score_home: int, 
country_away: str, score_away: int,
neutral: bool, ranking: Dict[str, int],
importance: int, sensitivity: int, home_buff: int) -> float:       
    if(neutral == False):
        probability_home = 1/(1+importance**(-(ranking[country_home]-ranking[country_away]+home_buff)/sensitivity))
    else:
        probability_home = 1/(1+importance**(-(ranking[country_home]-ranking[country_away])/sensitivity))
        
    ranking[country_home] += score_home
    ranking[country_away] += score_away #czy to automatycznie updatuje czy musze zwrocic ranking

    return probability_home