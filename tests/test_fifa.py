from core.rankings import FIFA93, FIFA06, FIFAcurrent
from core.preprocessing.pipelines import pipeline_fifa93_98, pipeline_fifa06_18, pipeline_fifa_current


df = pipeline_fifa93_98(2000)
estimate93_obj = FIFA93(df, 10, 400, 60)
df2, ranking = estimate93_obj.estimate93()
print(dict(sorted(ranking.items(), key=lambda item: item[1])))


df06, sim_years = pipeline_fifa06_18(2000,2023)
estimate06_obj = FIFA06(df06, 10, 400, 60, sim_years)
df06_2, ranking06 = estimate06_obj.estimate06()
print(ranking06)

dfcurrent = pipeline_fifa_current(2000)
estimatecurrent_obj = FIFAcurrent(dfcurrent)
dfcurrent_2, rankingcurrent = estimatecurrent_obj.estimate_current_fifa()
print(dict(sorted(rankingcurrent.items(), key=lambda item: item[1])))