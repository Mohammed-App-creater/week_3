import pandas as pd

file_path = r"C:\Users\yoga\code\10_Academy\week_3\data\raw\MachineLearningRating_v3.txt"
try:
    df = pd.read_csv(file_path, sep='|', nrows=1)
    cols = sorted(df.columns.tolist())
    for c in cols:
        print(c)
except Exception as e:
    print(e)
