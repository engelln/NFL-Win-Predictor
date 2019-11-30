from sklearn.tree import DecisionTreeClassifier
import pandas as pd
from Main.DecisionTreeGenerator import get_train_test_data
import matplotlib.pyplot as plt

# this script finds the optimal depth for the tree, and can graph the findings

# Editable Parameters vvvvv
data_dir = "D:\\Data\\NFL\\output\\FinalDataset.csv"
output_dir = "D:\\Data\\NFL\\output\\"
save_graph = False
# Editable Parameters ^^^^^


if __name__ == "__main__":
    data = pd.read_csv(data_dir)

    X_train, X_test, y_train, y_test = get_train_test_data(data)

    depth = range(1, 11)
    max_acc_settings = (-1, -1)
    accs = []
    # iterate each depth and find the best one over a 10 run average
    for d in depth:
        print(d)
        accuracy = 0
        for i in range(10):
            tree = DecisionTreeClassifier(max_depth=d)
            tree.fit(X_train, y_train)
            accuracy += tree.score(X_test, y_test)
        accuracy /= 10
        accs.append(accuracy)
        if accuracy > max_acc_settings[0]:
            max_acc_settings = (accuracy, d)
    print(f"Best Depth: {max_acc_settings[1]}\nAccuracy: {max_acc_settings[0]}")

    if save_graph:
        plt.plot(depth, accs)
        plt.xticks(depth)
        plt.title("Average Model Accuracy By Tree Depth")
        plt.xlabel("Tree Depth")
        plt.ylabel("Average Accuracy")
        plt.savefig(f"{output_dir}tree_depth_graph.png")



