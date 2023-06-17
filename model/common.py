import json
import os


def get_initial_params(initial_params_file="initial_params.json"):
    my_path = os.path.abspath(__file__).split(os.sep)
    my_path[-1] = initial_params_file
    with open(os.sep.join(my_path), "r", encoding="utf-8") as plik:
        initial_params = json.load(plik)
    return initial_params


def get_data(data_file="data.json"):
    my_path = os.path.abspath(__file__).split(os.sep)
    my_path[-1] = data_file
    with open(os.sep.join(my_path), "r", encoding="utf-8") as plik:
        data = json.load(plik)
    return data
