#Data From: https://www.ssa.gov/oact/babynames/limits.html

# Methodology:
# I read in the 2007 and 2020 SSA baby name datasets and ranked all names by birth count within each sex for 2007.
# Then, I merged the two datasets and filtered for names that were highly ranked in 2007 but had dropped out of the top 100 by 2020.
# I sorted these dropped names by their 2007 rank and selected the top 10 male and top 10 female names that saw significant decline.

import pandas as pd

df_2007 = pd.read_csv("yob2007.txt", names=["name", "sex", "count"])
df_2020 = pd.read_csv("yob2020.txt", names=["name", "sex", "count"])

df_2007["rank_2007"] = df_2007.groupby("sex")["count"].rank(ascending=False, method="first")
df_2020["rank_2020"] = df_2020.groupby("sex")["count"].rank(ascending=False, method="first")

merged = pd.merge(
    df_2007,
    df_2020[['name', 'sex', 'rank_2020']],
    on=['name','sex'],
    how='left'
)

male_names = merged[merged["sex"] == "M"]
female_names = merged[merged["sex"] == "F"]

male = merged[merged["sex"] == "M"]
top_male_dropped = male[
    (male["rank_2020"].isna()) | (male["rank_2020"] > 100)
    ].sort_values("rank_2007").head(10)

female = merged[merged["sex"] == "F"]
top_female_dropped = female[
    (female["rank_2020"].isna()) | (female["rank_2020"] > 100)
    ].sort_values("rank_2007").head(10)

print("Top 10 male names from 2007 that dropped out of top 100 in 2020:")
print(top_male_dropped[["name", "rank_2007", "rank_2020"]])

print("\nTop 10 female names from 2007 that dropped out of top 100 in 2020:")
print(top_female_dropped[["name", "rank_2007", "rank_2020"]])