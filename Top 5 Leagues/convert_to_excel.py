import pandas as pd

# Step 1: Load your CSV file
df = pd.read_csv(r"C:\Users\jprey\OneDrive\Escritorio\JP\KUL\5th Semester (Polimi)\MIT IDSS\Practice Projects\Top 5 Leagues\top_5_leagues_25_countries_cumulative.csv")
df.to_excel(r"C:\Users\jprey\OneDrive\Escritorio\JP\KUL\5th Semester (Polimi)\MIT IDSS\Practice Projects\Top 5 Leagues\top_5_leagues_25_countries_cumulative.xlsx", index=False)