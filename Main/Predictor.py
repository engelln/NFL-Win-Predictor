import pickle
import numpy as np


# Editable Parameters vvvvv
model_dir = "D:\\Data\\NFL\\output\\model.txt"
home = "NYG"
away = "CHI"
ht_pos = True
score = (0, 0)  # home, away
timeouts = (3, 3)  # home, away
qtr = 1
time = (15, 0)  # mins, secs
down_info = (1, 10)  # down x, y yards to first down
ydstotd = 75
week = 12
season = 2019
htst = (3,7,0)  # W, L, T
atst = (3,7,0)
# Editable Parameters ^^^^^


if __name__ == "__main__":
    file = open(model_dir, "rb")
    cls, le = pickle.load(file)
    ht = le.transform([home])
    at = le.transform([away])
    posteam = ht if ht_pos else at
    defteam = at if ht_pos else ht
    pred = cls.predict(np.array([ht, at, score[0], score[1], timeouts[0], timeouts[1], posteam, defteam, qtr,
                                time[0] * 60 + time[1], down_info[0], down_info[1], ydstotd, week, season,
                                htst[0], htst[1], htst[2], atst[0], atst[1], atst[2]]).reshape(1, -1))
    if pred[0] == 0:
        print(f"{home} will win")
    else:
        print(f"{away} will win")
