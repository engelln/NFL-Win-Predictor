from sklearn.tree import DecisionTreeClassifier
from sklearn import utils
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import pandas as pd


# testing sklearn classification


data = pd.read_csv("D:\\Data\\NFL\\FinalDataset.csv")
data.drop(["game_id"], inplace=True, axis=1)
data.dropna(inplace=True)

le = preprocessing.LabelEncoder()


for col in ["home_team", "away_team", "posteam", "defteam"]:
    data[col] = le.fit_transform(data[col])


data = utils.shuffle(data)

y = data["label"]
X = data.copy().drop("label", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

cls = DecisionTreeClassifier()
cls.fit(X_train, y_train)

accuracy = cls.score(X_test, y_test)
print(accuracy)
