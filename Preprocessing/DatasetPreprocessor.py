import pandas as pd
import os
import numpy as np

game_data_dir = "D:\\Data\\NFL\\game\\"
pbp_data_dir = "D:\\Data\\NFL\\pbp\\"
output_dir = "D:\\Data\\NFL\\output\\"


def combine_data_in_dir(path):
    print("Combining files in " + path)
    combined = pd.DataFrame()
    for file in os.listdir(path):
        combined = pd.concat([combined, pd.read_csv(path + file, low_memory=False)])
    return combined


def create_standings_data():
    print("Creating standings data")
    standings_data = []
    teams = set()

    for file in os.listdir(game_data_dir):
        data = pd.read_csv(game_data_dir + file, low_memory=False)
        yr = data["season"].unique()[0]
        teams = teams.union(data["home_team"].unique())
        season_total = {team: [0, 0, 0] for team in teams}
        for w in range(1, 18):
            week = data[data["week"] == w].copy()
            for team, standings in season_total.items():
                standings_data.append([team, yr, w, standings[0], standings[1], standings[2]])
            for i, game in week.iterrows():
                # win
                if game["home_score"] > game["away_score"]:
                    season_total[game["home_team"]][0] += 1
                    season_total[game["away_team"]][1] += 1
                # loss
                elif game["home_score"] < game["away_score"]:
                    season_total[game["home_team"]][1] += 1
                    season_total[game["away_team"]][0] += 1
                # tie
                else:
                    season_total[game["home_team"]][2] += 1
                    season_total[game["away_team"]][2] += 1

    return pd.DataFrame(standings_data, columns=["team", "season", "week", "win", "loss", "tie"])


def combine_standings_games():
    standings_data = create_standings_data()
    games_data = combine_data_in_dir(game_data_dir)
    print("Combining standings and games")

    ht_win = []
    ht_loss = []
    ht_tie = []
    at_win = []
    at_loss = []
    at_tie = []

    for i, game in games_data.iterrows():
        ht = standings_data[
            (standings_data["team"] == game["home_team"]) & (standings_data["season"] == game["season"]) & (
                        standings_data["week"] == game["week"])].iloc[0]
        at = standings_data[
            (standings_data["team"] == game["away_team"]) & (standings_data["season"] == game["season"]) & (
                        standings_data["week"] == game["week"])].iloc[0]
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

    return games_data


def combine_pbp_standings_games():
    pbp = combine_data_in_dir(pbp_data_dir)
    pbp = pbp[["game_id", "home_team", "away_team", "total_home_score",
                                         "total_away_score", "home_timeouts_remaining", "away_timeouts_remaining",
                                         "posteam", "defteam", "posteam_score", "defteam_score",
                                         "posteam_timeouts_remaining", "defteam_timeouts_remaining", "qtr",
                                         "quarter_seconds_remaining", "down", "ydstogo", "yardline_100"]]
    standings = combine_standings_games().drop(columns=["type", "state_of_game", "game_url", "home_team", "away_team"])
    print("Combining pbp and games")

    # need to add:
    # season, week, htwin, htloss, httie, atwin, atloss, attie, label

    return pd.merge(pbp, standings, on="game_id")


def create_final_dataset():
    data = combine_pbp_standings_games()
    print("Creating final dataset")
    data.dropna(inplace=True)
    data["label"] = 2
    data.loc[data["home_score"] > data["away_score"], "label"] = 0
    data.loc[data["home_score"] < data["away_score"], "label"] = 1
    data.drop(columns=["home_score", "away_score", "game_id"], inplace=True)
    data.replace("JAC", "JAX", inplace=True)
    data.replace("STL", "LA", inplace=True)
    data.replace("SD", "LAC", inplace=True)
    data.to_csv(output_dir+"FinalDataset.csv", index=False)


create_final_dataset()



