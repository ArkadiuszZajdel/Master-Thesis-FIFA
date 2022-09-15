from datetime import date
from core.preprocessing import load_basic_df, select_date, add_conditions
from core.fifa93_98 import estimate93
from core.preprocessing.pipelines import pipeline_fifa93_98

# df = load_basic_df()
# df = select_date(df, date(2000,1,1))
# df = add_conditions(df, [3,1,0])
df = pipeline_fifa93_98()
df2, ranking = estimate93(df, 10, 400, 60)
print(dict(sorted(ranking.items(), key=lambda item: item[1])))