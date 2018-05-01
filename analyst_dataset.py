from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import pickle
import numpy as np
import os

from utils import dataset

t_step_start = 99000
t_step_end = 99990
step = 10

X, y = dataset(t_step_start, t_step_end, step)
print(np.shape(X))
print(np.shape(y))
length = len(X)

data_dict = {}

data_X = set()
for x in X:
    data_X.add(str(x))
print(len(data_X))

#
# for idx, x in enumerate(X):
#     x = str(x)
#     y_ = str(y[idx])
#     if x in data_dict:
#         tmp = data_dict[x]
#         if y_ in tmp:
#             tmp[y_] = tmp[y_] + 1
#             # print("{} ------> {}, {}".format(x, y_, tmp[y_]))
#         else:
#             tmp[y_] = 1
#         data_dict[x] = tmp
#     else:
#         tmp = {}
#         tmp[y_] = 1
#         data_dict[x] = tmp
#
#
# print(len(data_dict))
# for key, value in data_dict.items():
#     if len(value) > 2:
#         for key_value, value_value in value.items():
#             print("{} ------------> {} : {}".format(key, key_value, value_value))
#
#
#

print("finished")