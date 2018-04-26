import os
import sys

t_start_step = 99900
predict_dir = "../data/new_data/{}".format(t_start_step)
if not os.path.exists(predict_dir):
    print("error predict file")
    sys.exit()

out_dir = "../data/out_data/{}".format(t_start_step)
if not os.path.exists(out_dir):
    os.mkdir(out_dir)
filenams = os.listdir(predict_dir)

for filename in filenams:
    path1 = os.path.join(predict_dir, filename)
    path2 = os.path.join(out_dir, filename)
    print(path1)
    print(path2)
    with open(path1) as f_read:
         lines = f_read.readlines()
         f_write = open(path2, 'w')
         f_write.write("Title='LBM Lid Driven Flow'\n"+"VARIABLES=X, Y, U, V, R, P, M,\n"+"ZONE T='BOX, I=101, J=101, F=POINT\n")
         for line in lines:
            datas = line.strip().replace('\t', ' ').split(" ")

            x = int(datas[0]) % 101
            y = int(datas[0]) // 101

            f_write = open(path2, 'a')
            f_write.write(str(x)+'\t'+str(y)+'\t'+str(datas[9])+'\t'+str(datas[10])+'\t'+str(datas[11])+'\t'+str(datas[12])+'\t'+str(datas[13])+'\n')
