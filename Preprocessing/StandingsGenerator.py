import pandas as pd
import os


# Team, year, week, wins, losses, ties

# for file in dir:
#

dir = "D:\\Data\\NFL\\game\\"

standings_data = []
teams = set()

for file in os.listdir(dir):
    data = pd.read_csv(dir+file, low_memory=False)
    yr = data["season"].unique()[0]
    teams = teams.union(data["home_team"].unique()).union(data["away_team"].unique())
    season_total = {team:[0,0,0] for team in teams}
    for w in range(1, 18):
        week = data[data["week"] == w].copy()
        for team, standings in season_total.items():
            #print([team, yr, w, standings[0], standings[1], standings[2]])
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


pd.DataFrame(standings_data).to_csv(dir+"standings2.csv", index=False)

