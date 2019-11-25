import pandas as pd
import os



pbp_dir = "D:\\Data\\NFL\\pbp2.csv"
standings_dir = "D:\\Data\\NFL\\GamesStandings.csv"

pbp = pd.read_csv(pbp_dir, low_memory=False)
standings = pd.read_csv(standings_dir)
#
# pbp = pbp[["game_id", "home_team", "away_team", "total_home_score", "total_away_score",
#            "home_timeouts_remaining", "away_timeouts_remaining", "posteam", "defteam", "posteam_score", "defteam_score",
#            "posteam_timeouts_remaining", "defteam_timeouts_remaining", "qtr", "quarter_seconds_remaining", "down",
#            "ydstogo", "yardline_100", "play_type"]]
#
# pbp.to_csv("D:\\Data\\NFL\\pbp2.csv")



ht_win = []
ht_loss = []
ht_tie = []
at_win = []
at_loss = []
at_tie = []
ht_final = []
at_final = []
label = []

for i, play in pbp.iterrows():
    print(i)
    # id = locate play game id
    id = play["game_id"]
    # find corresponding game in gamesstandings
    gs_game = standings[standings["game_id"] == id].iloc[0]
    # add all values to corresponding lists
    ht_win.append(gs_game["ht_win"])
    ht_loss.append(gs_game["ht_loss"])
    ht_tie.append(gs_game["ht_tie"])
    at_win.append(gs_game["at_win"])
    at_loss.append(gs_game["at_loss"])
    at_tie.append(gs_game["at_tie"])
    ht_final.append(gs_game["home_score"])
    at_final.append(gs_game["away_score"])
    if gs_game["home_score"] > gs_game["away_score"]:
        label.append(0)
    elif gs_game["home_score"] < gs_game["away_score"]:
        label.append(1)
    else:
        label.append(2)

pbp["ht_win"] = ht_win
pbp["ht_loss"] = ht_loss
pbp["ht_tie"] = ht_tie
pbp["at_win"] = at_win
pbp["at_loss"] = at_loss
pbp["at_tie"] = at_tie
pbp["ht_final"] = ht_final
pbp["at_final"] = at_final
pbp["label"] = label

pbp.to_csv("D:\\Data\\NFL\\FinalDataset.csv")