import pandas as pd


df = pd.read_json('categories.json')

print(df['link'].values.tolist())