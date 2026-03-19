import pandas as pd
import numpy as np

df = pd.read_csv("raw_data/31622-0001-Data.tsv", sep="\t", low_memory=False)

candidate_cols = [
    "IDNUM",
    "CH4WJSS22",      # reading standard score
    "CH4LR_CORSCOR",  # focused attention score
    "CM4HHINC",       # mother household income
    "CM4EDU"          # mother education
]

keep_cols = [c for c in candidate_cols if c in df.columns]
missing_cols = [c for c in candidate_cols if c not in df.columns]

print("Keeping columns:", keep_cols)
print("Missing columns:", missing_cols)

small_df = df[keep_cols].copy()

missing_codes = [-9, -8, -7, -6, -5, -4, -3, -2, -1]
small_df = small_df.replace(missing_codes, np.nan)

rename_map = {
    "IDNUM": "id",
    "CH4WJSS22": "reading_standard_score",
    "CH4LR_CORSCOR": "focused_attention_score",
    "CM4HHINC": "mother_household_income",
    "CM4EDU": "mother_education"
}
small_df = small_df.rename(columns=rename_map)

small_df.to_csv("data/child_dev_subset.csv", index=False)

analysis_df = small_df.dropna(subset=["reading_standard_score", "focused_attention_score"]).copy()
analysis_df.to_csv("data/child_dev_analysis_ready.csv", index=False)

print("\nCleaned subset shape:", small_df.shape)
print("Analysis-ready shape:", analysis_df.shape)
print("\nPreview:")
print(analysis_df.head())
print("\nSummary statistics:")
print(analysis_df.describe())