import pandas as pd
import os

# This script combines and cleans up the provided game and play by play data

# Editable Parameters vvvvv
game_data_dir = "D:\\Data\\NFL\\game\\"
pbp_data_dir = "D:\\Data\\NFL\\pbp\\"
output_dir = "D:\\Data\\NFL\\output\\"
# Editable Parameters ^^^^^


# combines data in different csv files in the same directory into a single pandas dataframe
def combine_data_in_dir(path):
    print("Combining files in " + path)
    combined = pd.DataFrame()
    for file in os.listdir(path):
        combined = pd.concat([combined, pd.read_csv(path + file, low_memory=False)])
    return combined


# creates a dataframe with week by week standings for each team
def create_standings_data():
    print("Creating standings data")
    standings_data = []
    teams = set()

    # each csv file in the dir consists of a different season/year
    for file in os.listdir(game_data_dir):
        data = pd.read_csv(game_data_dir + file, low_memory=False)
        # all games in this file will have the same season
        yr = data["season"].unique()[0]
        # get all team abbreviations for that year(they do occasionally change, this is fixed in create_final_dataset())
        teams = teams.union(data["home_team"].unique())
        # initialize standings for each team this season
        season_total = {team: [0, 0, 0] for team in teams}
        # each regular season has 17 weeks
        for w in range(1, 18):
            # grab this weeks games
            week = data[data["week"] == w].copy()
            # record standings for that week
            # they are recorded before updating because
            # in game you technically see the previous week's standings for both teams
            for team, standings in season_total.items():
                standings_data.append([team, yr, w, standings[0], standings[1], standings[2]])

            # update the standings
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


# combines the standings data with the data for each game
def combine_standings_games():
    standings_data = create_standings_data()
    games_data = combine_data_in_dir(game_data_dir)
    print("Combining standings and games")

    # columns being added to the game data
    ht_win = []
    ht_loss = []
    ht_tie = []
    at_win = []
    at_loss = []
    at_tie = []

    # generate the data for each column
    for i, game in games_data.iterrows():
        # match games and teams by the team abbreviation, season, and week
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

# combine the standings and games data with the play by play data
def combine_pbp_standings_games():
    pbp = combine_data_in_dir(pbp_data_dir)
    # define the columns to keep from pbp data
    pbp = pbp[["game_id", "home_team", "away_team", "total_home_score", "total_away_score", "home_timeouts_remaining",
               "away_timeouts_remaining", "posteam", "defteam", "qtr", "quarter_seconds_remaining", "down", "ydstogo",
               "yardline_100"]]

    # define the columns to remove from game/standings data
    standings = combine_standings_games().drop(columns=["type", "state_of_game", "game_url", "home_team", "away_team"])
    print("Combining pbp and games")

    # this can be combined much easier because both datasets have matching ids
    return pd.merge(pbp, standings, on="game_id")


# creates and saves the final dataset
def create_final_dataset():
    data = combine_pbp_standings_games()
    print("Creating final dataset")
    # drop samples with any na's, there's almost 500k samples so it won't hurt to lose a few
    data = data.dropna()
    # label samples 0: HT win, 1: AT win, 2: tie
    data["label"] = 2
    data.loc[data["home_score"] > data["away_score"], "label"] = 0
    data.loc[data["home_score"] < data["away_score"], "label"] = 1
    # throw out ties because the decision tree wouldn't learn them
    data = data[data["label"] != 2]
    # drop scores used in label calculation
    data = data.drop(columns=["home_score", "away_score"])
    # update abbreviations from older seasons
    data = data.replace("JAC", "JAX")
    data = data.replace("STL", "LA")
    data = data.replace("SD", "LAC")
    data.to_csv(output_dir+"FinalDataset.csv", index=False)


if __name__ == "__main__":
    create_final_dataset()



