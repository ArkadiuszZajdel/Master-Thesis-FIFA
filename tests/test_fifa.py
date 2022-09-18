from core.rankings import estimate93, Estimate06
from core.preprocessing.pipelines import pipeline_fifa93_98, pipeline_fifa06_18


df = pipeline_fifa93_98()
df2, ranking = estimate93(df, 10, 400, 60)
print(dict(sorted(ranking.items(), key=lambda item: item[1])))


df06, sim_years = pipeline_fifa06_18(2000,2023)
estimate06_obj = Estimate06(df06, 10, 400, 60, sim_years)
df06_2, ranking06 = estimate06_obj.estimate06()
print(ranking06)