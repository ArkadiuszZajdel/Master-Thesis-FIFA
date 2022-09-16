from core.fifa import estimate93
from core.preprocessing.pipelines import pipeline_fifa93_98, pipeline_fifa06_18


df = pipeline_fifa93_98()
df2, ranking = estimate93(df, 10, 400, 60)
print(dict(sorted(ranking.items(), key=lambda item: item[1])))

print(pipeline_fifa06_18())