import pandas as pd
import os


game_data_dir = "D:\\Data\\NFL\\game\\"
pbp_data_dir = "D:\\Data\\NFL\\pbp\\"
output_dir = "D:\\Data\\NFL\\output\\"


def combine_data_in_dir(path):
    combined = pd.DataFrame()
    for file in os.listdir(path):
        combined = pd.concat([combined, pd.read_csv(path + file, low_memory=False)])
    return combined


def create_standings_data():
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

combine_standings_games().to_csv(output_dir+"standingsgames.csv", index=False)



