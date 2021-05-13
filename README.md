# NFL-Win-Predictor
Classification with NFL Data.

# Introduction
This is a program used to predict the winning team of NFL games as the game is in progress by entering different stats as the game progresses. This project was created in Fall 2019 as a part of my Data Mining class. 

Using NFL play by play data found in [this repository](https://github.com/ryurko/nflscrapR-data), I trained a decision tree based classifier to predict the outcome of games in progress, using stats such as the teams, the score, timeouts remaining, current quarter, time remaining, the down of the play, the yards to go, the week of play, the season year, and the team standings.

The results of the project showed around 75% accuracy average when testing, although I do not believe it to be the best methodology. To prevent overfitting, I excluded plays from the same game in training and testing, i.e. if plays from one game are in the training dataset, other plays from that game will not be in the testing dataset. However, I believe the fact that multiple plays from the same game in a single dataset could still have some effect on results, but have not tested this.

# Requirements
This project requires the following python packages to run:
1. numpy
2. scikit-learn
3. matplotlib
4. pandas

# Setup
There are 4 main functionalities this repository provides:
1. Dataset generation with DatasetPreprocessor.py
2. Decision tree optimal parameter searching with TreeParameterSearch.py
3. Decision tree generation with DecisionTreeGenerator.py
4. Example production implementation for making predictions with Predictor.py

The last 3 are pretty self explanitory, the parameters inside each file just need to be configured.

For the preprocessor, you need to first clone the data from [this repository](https://github.com/ryurko/nflscrapR-data).
That repository contains 2 types of data: game data, which contains the data about each NFL game, and Play by Play data, which contains the data about every play of every game. The data is separated by year in different CSV files, and also separated by preseason, regular season, and postseason (playoffs). This project only examined the regular season data.

1. Create a directory for both game data and play by play data, and for output.
2. Drag all CSV files of the respective type into each folder. For example, if using regular season data, all CSV files in the game data folder should be named "reg_games_{year}.csv" and all play by play files should be "reg_pbp_{year}.csv".
3. Configure the variables at the top of the DatasetPreprocessor.py script to match the created directories.
4. Run the script. This will combine all the data into one big CSV file, which should be used in the other scripts.
