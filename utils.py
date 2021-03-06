from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import pickle
import numpy as np

import os

path_state_format_pickle = "../data/pickle/{}.pkl"
path_state_format = "../data/dat_rel/{}.dat"
path_relation_format = "../data/dat_rel/{}.dat"
path_pkl = "../data/dat_rel/{}.pkl"
path_new_data = "../data/new_data/{}.dat"

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



# dataset from t-step-start-th to t_step_end-th, x: 18-D, y: 2-D
def dataset(t_step_start, t_step_end, step):
    data_ = []
    for i in range(t_step_start, t_step_end + 1, step):
        f = open(path_state_format_pickle.format(i), "rb")
        # print(f)
        state = pickle.load(f)
        # print(type(state))
        data_.append(state)
        f.close()
    X = []
    Y = []
    for j in range(len(data_) - 1):
        # print(type(data_[j]))
        for key, value in data_[j].items():
            x = value
            y = data_[j + 1][key][8:10]
            X.append(x)
            Y.append(y)
    return np.array(X), np.array(Y)

# get the idx-th step's lattic state
def get_step_idx_state(idx):
    path = path_relation_format.format(idx)
    # print(path)
    lattic_relation = preprocess(path)
    path = path_state_format.format(idx)
    state_0 = state(idx, lattic_relation, path)
    return state_0

# convert the dataset and save as .pkl
def data_to_pickle():
    t_step = 99990
    path = path_relation_format.format(0)
    lattic_relation = preprocess(path=path)
    print(lattic_relation[10])
    print(lattic_relation.__len__())
    for idx in range(0, t_step + 1, 10):
        print("idx: ", idx)
        f = open(path_pkl.format(idx), "wb")
        path = path_state_format.format(idx)
        idx_state = state(idx, lattic_relation, path)
        # if idx == 10:
        #     print(idx_state[0])
        pickle.dump(idx_state, f)
        f.close()

# convert the origin data with format []
# original data [lattice lattice_1 lattice_5 lattice_2 lattice_6 lattice_3 lattice_7 lattice_4 lattice_8 u v rho p mach]
### lattice_1 lattice_5  lattice_2
### lattice_6 lattice    lattice_3
### lattice_7 lattice_4  lattice_8


def get_origin_data(path):
    # path = path_relation_format.format(idx)
    # print(path)
    f = open(path, "r")
    origin_data = []
    for line in f.readlines():
        data = line.split()
        lattice = int(data[0])
        lattic_1 = int(data[1])
        lattic_5 = int(data[2])
        lattic_2 = int(data[3])
        lattic_6 = int(data[4])
        lattic_3 = int(data[5])
        lattic_7 = int(data[6])
        lattic_4 = int(data[7])
        lattic_8 = int(data[8])
        u = float(data[9])
        v = float(data[10])
        rho = float(data[11])
        p = float(data[12])
        mach = float(data[13])
        # print(lattice, p, mach)
        origin_data.append((lattice, lattic_1, lattic_5, lattic_2, lattic_6, lattic_3,
                            lattic_7, lattic_4, lattic_8, u, v, rho, p, mach))
    return np.array(origin_data)

def preprocess(path):
    # path = path_relation_format.format(idx)
    f = open(path, "r")
    lattic_relation = {}
    for line in f.readlines():
        data = line.split()
        lattice = int(data[0])
        lattic_1 = int(data[1])
        lattic_5 = int(data[2])
        lattic_2 = int(data[3])
        lattic_6 = int(data[4])
        lattic_3 = int(data[5])
        lattic_7 = int(data[6])
        lattic_4 = int(data[7])
        lattic_8 = int(data[8])
        u = float(data[9])
        v = float(data[10])
        rho = float(data[11])
        p = float(data[12])
        mach = float(data[13])
        # print(lattice, p, mach)
        lattic_relation[lattice] = [lattic_1, lattic_2, lattic_3, lattic_4, lattice, lattic_5, lattic_6, lattic_7, lattic_8]
    return lattic_relation


def state(idx, lattic_relation, path):
    # f = open(path_state_format.format(idx), "r")
    f = open(path, "r")
    t_step_state = {}
    tmp_state = {}
    for line in f.readlines():
        data = line.split()
        lattic = int(data[0])
        u = float(data[9])
        v = float(data[10])
        rho = float(data[11])
        p = float(data[12])
        mach = float(data[13])
        tmp_state[lattic] = [u, v]

    for lattic, relation in lattic_relation.items():
        # print("lattic", lattic)
        lattic_state = []
        for lattic_idx in relation:
            u, v = tmp_state[lattic_idx]
            lattic_state.append(u)
            lattic_state.append(v)
        t_step_state[lattic] = lattic_state
    return t_step_state