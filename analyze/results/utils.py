import os
import sys

import matplotlib.pyplot as plt


def add_path(folder="model"):
    current_path = os.path.dirname(__file__).split(os.sep)
    while len(current_path):
        if folder in os.listdir(os.sep.join(current_path)):
            sys.path.append(os.sep.join(current_path))
            return
        current_path.pop()
    print(f"WOOPS: probably bad folder arg: {folder}")


def get_path_with(folder="model"):
    current_path = os.path.dirname(__file__).split(os.sep)
    while len(current_path):
        if folder in os.listdir(os.sep.join(current_path)):
            return os.sep.join(current_path)
        current_path.pop()
    print(f"WOOPS: probably bad folder arg: {folder}")


def save_in(name, folder="pictures", fig=None):
    target = [get_path_with(folder), folder, name]
    if fig is None:
        plt.savefig(os.sep.join(target), bbox_inches="tight")
    else:
        fig.savefig(os.sep.join(target), bbox_inches="tight")
    print(f"saved as: {target}")
