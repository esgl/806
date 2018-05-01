from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import pickle
import numpy as np
import os

t_step_start = 100
t_step_end = 200
step = 10

path_state_format_pickle = "../../data/pickle/{}.pkl"
path_state_format = "../../data/dat_rel/{}.dat"
path_relation_format = "../../data/dat_rel/{}.dat"
path_pkl = "../../data/dat_rel/{}.pkl"
path_new_data = "../../data/new_data/{}.dat"


def vec_to_str(vec):
    vec_to_s = ""
    for idx in range(len(vec)-1):
        vec_to_s += str(vec[idx]) + "_"
    vec_to_s += str(vec[idx])
    return vec_to_s

def str_to_vec(str_):
    s = str_.split("_")
    return np.array(s)

def dataset_new(t_step_start, t_step_end, step):
    data_ = {}
    for i in range(t_step_start, t_step_end, step):
        print(path_state_format_pickle.format(i))
        f = open(path_state_format_pickle.format(i), "rb")
        f_next = open(path_state_format_pickle.format(i + step), "rb")

        state = pickle.load(f)
        state_next = pickle.load(f_next)
        for idx, (key, value) in enumerate(state.items()):
            data_[vec_to_str(value)] = vec_to_str(state_next[key][8:10])
        f.close()
        f_next.close()
    X = []
    Y = []
    for key, value in data_.items():
        x = np.array(str_to_vec(key), dtype=float)
        y = np.array(str_to_vec(value), dtype=float)
        X.append(x)
        Y.append(y)
    path = "../../data/sample"
    if not os.path.exists(path):
        os.mkdir(path)
    f_pickle = open("{}/{}_{}_{}.pkl".format(path, t_step_start, t_step_end, step), "wb")
    pickle.dump((X, Y), f_pickle)
    f_pickle.close()

    return (np.array(X), np.array(Y))


X, Y = dataset_new(t_step_start, t_step_end, step)
print("X")
print(X)
print("Y")
print(Y)
print(len(X))
print(len(Y))