from sklearn.tree import DecisionTreeClassifier
import pandas as pd
from Main.DecisionTreeGenerator import get_train_test_data

# Editable Parameters vvvvv
data_dir = "D:\\Data\\NFL\\output\\FinalDataset.csv"
# Editable Parameters ^^^^^


if __name__ == "__main__":
    data = pd.read_csv(data_dir)

    X_train, X_test, y_train, y_test = get_train_test_data(data)

    criterion = ["gini", "entropy"]
    depth = range(1, 20)
    max_acc_settings = (-1, "", -1)
    for c in criterion:
        for d in depth:
            print(c, d)
            accuracy = 0
            for i in range(10):
                tree = DecisionTreeClassifier(criterion=c, max_depth=d)
                tree.fit(X_train, y_train)
                accuracy += tree.score(X_test, y_test)
            accuracy /= 10
            if accuracy > max_acc_settings[0]:
                max_acc_settings = (accuracy, c, d)
    print(f"Best Criterion: {max_acc_settings[1]}\nBest Depth: {max_acc_settings[2]}")
