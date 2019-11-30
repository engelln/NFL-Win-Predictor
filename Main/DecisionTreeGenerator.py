from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn import utils
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt

# This script creates the decision tree and provides some metrics about it

# Editable Parameters vvvvv
dataset_dir = "D:\\Data\\NFL\\output\\FinalDataset.csv"
output_dir = "D:\\Data\\NFL\\output\\"
save_model = False  # set to True to have the tree saved to a txt file
save_tree_png = False  # set to True to save an image of the tree
plot_qtr_acc = False  # set to True to save a graph of tree accuracy by quarter
# Editable Parameters ^^^^^

le = preprocessing.LabelEncoder()


# final preparation of the dataset before being fed into the tree for training
# splits dataset into training and testing data by game rather than random plays to prevent overfitting
def get_train_test_data(data, test_split=.25):
    # convert team abbreviations to numbers for training purposes
    for col in ["home_team", "away_team", "posteam", "defteam"]:
        data[col] = le.fit_transform(data[col])
    # calculate the number of games to use for the test set
    test_games = int(len(data["game_id"].unique()) * test_split)
    # choose games for the test set
    test_game_ids = np.random.choice(data["game_id"].unique(), size=test_games, replace=False)
    # get test set
    test_data = data[data["game_id"].isin(test_game_ids)]
    # training set = data - test set
    train_data = data[~data.isin(test_data)].dropna()
    # drop id from both sets its no longer needed
    test_data = test_data.drop("game_id", axis=1)
    train_data = train_data.drop("game_id", axis=1)
    # shuffle both sets
    test_data = utils.shuffle(test_data)
    train_data = utils.shuffle(train_data)
    # separate labels
    X_train, y_train = train_data.drop("label", axis=1), train_data["label"]
    X_test, y_test = test_data.drop("label", axis=1), test_data["label"]
    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    data = pd.read_csv(dataset_dir)

    X_train, X_test, y_train, y_test = get_train_test_data(data)

    # decision tree with max depth 6 using gini index to determine best split
    cls = DecisionTreeClassifier(max_depth=6, criterion='gini')
    cls.fit(X_train, y_train)

    # save optional metrics
    if save_tree_png:
        import graphviz
        dot = tree.export_graphviz(cls, out_file=None, feature_names=X_train.columns.values, class_names=["Home Win", "Away Win"], filled=True)
        graphviz.Source(dot, filename="tree", format="png", directory=output_dir).render()

    if save_model:
        save = (cls, le)
        out = open(output_dir + "model.txt", "wb")
        pickle.dump(save, out)

    if plot_qtr_acc:
        qtrs = range(1, 5)
        accs = []
        for q in qtrs:
            d = X_test.copy()
            d["label"] = y_test
            d = d[d["qtr"] == q]
            d, dl = d.drop("label", axis=1), d["label"]
            accs.append(cls.score(d, dl))

        plt.plot(qtrs, accs)
        plt.xlabel("Quarter")
        plt.ylabel("Accuracy")
        plt.title("Model Accuracy By Quarter")
        plt.savefig(f"{output_dir}accuracy_by_qtr_graph.png")

    # print accuracies and confusion matrix
    train_accuracy = cls.score(X_train, y_train)
    test_accuracy = cls.score(X_test, y_test)

    print(f"Train Accuracy: {train_accuracy}")
    print(f"Test  Accuracy: {test_accuracy}")

    print("Confusion Matrix:")
    cm = confusion_matrix(y_test, cls.predict(X_test))
    print(cm)
    print("Scaled Confusion Matrix:")
    print(cm.astype("float") / cm.sum(axis=1)[:, np.newaxis])

