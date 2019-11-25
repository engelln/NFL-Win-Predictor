import pandas as pd
import os



standings = "D:\\Data\\NFL\\standings.csv"
games = "D:\\Data\\NFL\\games2.csv"

games_data = pd.read_csv(games)
standings_data = pd.read_csv(standings)

ht_win = []
ht_loss = []
ht_tie = []
at_win = []
at_loss = []
at_tie = []

# giants 2019 week 3
res = standings_data[(standings_data["team"] == "NYG") & (standings_data["season"] == 2019) & (standings_data["week"] == 3)].copy()
#print(res.iloc[0])

for i, game in games_data.iterrows():
    ht = standings_data[(standings_data["team"] == game["home_team"]) & (standings_data["season"] == game["season"]) & (standings_data["week"] == game["week"])].iloc[0]
    at = standings_data[(standings_data["team"] == game["away_team"]) & (standings_data["season"] == game["season"]) & (standings_data["week"] == game["week"])].iloc[0]
    ht_win.append(ht["win"])
    ht_loss.append(ht["loss"])
    ht_tie.append(ht["tie"])
    at_win.append(at["win"])
    at_loss.append(at["loss"])
    at_tie.append(at["tie"])

games_data["ht_win"] = ht_win
games_data["ht_loss"] = ht_loss
games_data["ht_tie"] = ht_tie
games_data["at_win"] = at_win
games_data["at_loss"] = at_loss
games_data["at_tie"] = at_tie

games_data.to_csv("D:\\Data\\NFL\\GamesStandings2.csv")
