from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import pickle
import numpy as np
import os

#开始导入和构建序列模型
from keras.models import Sequential
#向模型中添加 Dense（full connected layer）
from keras.layers import Dense
from keras.layers import Activation
from keras.layers import regularizers, BatchNormalization
from keras import losses

# from preprocess import preprocess, state, get_origin_data
path_state_format_pickle = "../data/pickle/{}.pkl"
path_state_format = "../data/dat_rel/{}.dat"
path_relation_format = "../data/dat_rel/{}.dat"
path_pkl = "../data/dat_rel/{}.pkl"
path_new_data = "../data/new_data/{}.dat"

t_step_start = 0
t_step_end = 99990
step = 10

from utils import dataset, get_step_idx_state, get_origin_data

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'



def build_model():
    model = Sequential()

    model.add(Dense(100, input_shape=(18,), kernel_regularizer=regularizers.l2(0.01)))
    model.add(BatchNormalization())
    model.add(Activation("relu"))

    model.add(Dense(100, kernel_regularizer=regularizers.l2(0.01)))
    model.add(BatchNormalization())
    model.add(Activation("relu"))

    # 全链接层 输出维度
    model.add(Dense(1))

    # 指定优化器和损失函数
    model.compile(optimizer="sgd", loss=losses.mean_squared_error)
    return model



def getData():

    X, Y = dataset(t_step_start, t_step_end, step)
    len_X = len(X)
    print(len_X)
    X_ = []
    Y_ = []
    for idx, x in enumerate(X):
        # print(idx)
        if not(np.sum(x) == 0. and (np.sum(Y[idx])) == 0.):
            X_.append(x)
            Y_.append(Y[idx])
    X = np.array(X_)
    Y = np.array(Y_)
    len_X = len(X)
    print(len_X)
    indics = np.arange(len_X)
    np.random.shuffle(indics)
    X = X[indics]
    Y = Y[indics]
    # print(type(indics))
    # print(indics[0:10])
    ratio = 0.6
    nb_train_samples = int(len_X * ratio)

    X_train = X[:nb_train_samples]
    y_train = Y[:nb_train_samples]
    X_test = X[nb_train_samples:]
    y_test = Y[nb_train_samples:]

    return X_train, y_train, X_test, y_test


if __name__ == "__main__":
    X_train, y_train, X_test, y_test = getData()
    y_train_u = y_train[:,0, np.newaxis]
    print(y_train_u.shape)
    y_test_u = y_test[:,0, np.newaxis]
    y_train_v = y_train[:,1, np.newaxis]
    y_test_v = y_test[:,1, np.newaxis]
    model_u = build_model()
    model_v = build_model()
    print("training.........")
    if not os.path.exists("../model/ml_cfd_u_{}.h5".format(t_step_start)):
        model_u.fit(X_train, y_train_u, epochs=2, batch_size=128)
        model_u.save_weights("../model/ml_cfd_u_{}.h5".format(t_step_start))
    else:
        model_u.load_weights("../model/ml_cfd_u_{}.h5".format(t_step_start))

    score = model_u.evaluate(X_test, y_test_u, batch_size = 128)

    if not os.path.exists("../model/ml_cfd_v_{}.h5".format(t_step_start)):
        model_v.fit(X_train, y_train_v, epochs=2, batch_size=128)
        model_v.save_weights("../model/ml_cfd_v_{}.h5".format(t_step_start))
    else:
        model_v.load_weights("../model/ml_cfd_v_{}.h5".format(t_step_start))

    score = model_v.evaluate(X_test, y_test_v, batch_size = 128)

    predict = True
    # 打印测试模型的性能
    print(score)

    if predict:

        step_0_state = get_step_idx_state(t_step_start)
        step_0_state_ = [value for _, value in step_0_state.items()]
        step_0_state_ = np.array(step_0_state_)
        state_ = step_0_state_
        dir = "../data/new_data/{}".format(t_step_start)
        if not os.path.exists(dir):
            os.mkdir(dir)
        for step in range(t_step_start, t_step_end + 1, 10):
            print("predict step", step)
            state_next_u = model_u.predict(state_)
            state_next_v = model_v.predict(state_)
            path = path_state_format.format(step)
            origin_state = get_origin_data(path)
            assert len(state_next_u) == np.shape(origin_state)[0]
            f_new_state_path = "{}/{}.dat".format(dir, step)
            # f_new_state = open(path_new_data.format(step), 'w')
            f_new_state = open(f_new_state_path, "w")
            for no in range(len(state_next_u)):
                if np.sum(state_[no]) == 0.:
                    origin_state[no][9] = 0.
                    origin_state[no][10] = 0.
                else:
                    origin_state[no][9] = state_next_u[no]
                    origin_state[no][10] = state_next_v[no]
                str_ = ""
                for j in range(np.shape(origin_state)[1]):
                    if j < 9:
                        str_ = str_ + str(int(origin_state[no][j])) + "\t"
                    else:
                        str_ = str_ + str(origin_state[no][j]) + "\t"
                # print("str ", str_)
                f_new_state.writelines(str_ + "\n")
            f_new_state.close()
            # path = "{}/{}.dat".format(dir, step)
            # print(path)
            state_ = get_step_idx_state(step)
            # print(state_)
            state_ = [value for _, value in state_.items()]
            state_ = np.array(state_)

