import pandas as pd
import os


data = pd.DataFrame()
dir = "D:\\Data\\NFL\\game\\"

for file in os.listdir(dir):
    data = pd.concat([data, pd.read_csv(dir+file, low_memory=False)])


data.to_csv(dir+"games2.csv", index=None, header=True)