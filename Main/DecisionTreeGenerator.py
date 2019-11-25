from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn import utils
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
import pandas as pd
import pickle
import numpy as np

# Editable Parameters vvvvv
dataset_dir = "D:\\Data\\NFL\\output\\FinalDataset.csv"
output_dir = "D:\\Data\\NFL\\output\\"
save_model = True
save_tree_png = True
# Editable Parameters ^^^^^


def get_train_test_data(data, test_split=.25):
    test_games = int(len(data["game_id"].unique()) * test_split)
    test_game_ids = np.random.choice(data["game_id"].unique(), size=test_games, replace=False)
    test_data = data[data["game_id"].isin(test_game_ids)]
    train_data = data[~data.isin(test_data)].dropna()
    test_data = test_data.drop("game_id", axis=1)
    train_data = train_data.drop("game_id", axis=1)
    test_data = utils.shuffle(test_data)
    train_data = utils.shuffle(train_data)
    X_train, y_train = train_data.drop("label", axis=1), train_data["label"]
    X_test, y_test = test_data.drop("label", axis=1), test_data["label"]
    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    data = pd.read_csv(dataset_dir)
    # throw out ties because the decision tree won't learn them
    data = data[data["label"] != 2]

    le = preprocessing.LabelEncoder()

    for col in ["home_team", "away_team", "posteam", "defteam"]:
        data[col] = le.fit_transform(data[col])

    X_train, X_test, y_train, y_test = get_train_test_data(data)

    cls = DecisionTreeClassifier(criterion='entropy', max_depth=7)
    cls.fit(X_train, y_train)

    if save_tree_png:
        import graphviz

        dot = tree.export_graphviz(cls, out_file=None)
        graphviz.Source(dot, filename="tree", format="png", directory=output_dir).render()

    if save_model:
        save = (cls, le)
        out = open(output_dir + "model.txt", "wb")
        pickle.dump(save, out)

    train_accuracy = cls.score(X_train, y_train)
    test_accuracy = cls.score(X_test, y_test)

    print(f"Train Accuracy: {train_accuracy}")
    print(f"Test  Accuracy: {test_accuracy}")

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, cls.predict(X_test)))
    print(confusion_matrix(y_test, cls.predict(X_test)))
