import os


filenams = os.listdir("../data/dat_in")
for filename in filenams:
    # print(filename)
    path1 = os.path.join("../data/dat_in/"+filename)
    path2 = os.path.join("../data/dat_test/"+filename)
    print(path1)
    with open(path1) as f_read:
        # f_write = open(path2, 'w')
        # f_write.write("Title='LBM Lid Driven Flow'\n" + "VARIABLES=X, Y, U, V, R, P, M,\n" + "ZONE T='BOX, I=101, J=101, F=POINT\n")
        lines = f_read.readlines()
        for line in lines:
            datas = line.strip().replace('\t',' ').split(' ')
            # print(datas[0]+' '+datas[1]+' '+datas[2]+' '+datas[3]+' '+datas[4]+' '+datas[5]+' '+datas[6])
            # 左上角
            f_write = open(path2, 'a')
            if (int(datas[0])==0)&(int(datas[1])==0):
                # f_write = open(path2, 'a')
                   f_write.write("0"+'\t'+"101"+'\t'+"0"+'\t'+"0"+'\t'+"0"+
                   # Z
                              '\t'+"0"+'\t'+"0"+'\t'+"1"+'\t'+"102"+'\t'+
                              str(datas[2])+'\t'+str(datas[3])+'\t'+str(datas[4])+'\t'+str(datas[5])+'\t'+str(datas[6])+'\n')
            # 右上角
            elif (int(datas[0])==0)&(int(datas[1])==100):
                # f_write = open(path2, 'a')
                f_write.write("10100" + '\t' + "0" + '\t' + "0" + '\t' + "0" + '\t' + "0" +
                              '\t' + "10000" + '\t' + "10001" + '\t' + "10101" + '\t' + "0" +'\t'+
                              str(datas[2]) + '\t' + str(datas[3]) + '\t' + str(datas[4]) + '\t' + str(datas[5]) + '\t' + str(datas[6]) + '\n')
            # 左下角
            elif (int(datas[0]) == 100) & (int(datas[1]) == 0):
                # f_write = open(path2, 'a')
                f_write.write("100" + '\t' + "201" + '\t' + "200" + '\t' + "99" + '\t' + "0" +
                              '\t' + "0" + '\t' + "0" + '\t' + "0" + '\t' + "0" + '\t' +
                              str(datas[2]) + '\t' + str(datas[3]) + '\t' + str(datas[4]) + '\t' + str(datas[5]) + '\t' + str(datas[6]) + '\n')
            # 右下角
            elif (int(datas[0]) == 100) & (int(datas[1]) == 100):
                # f_write = open(path2, 'a')
                f_write.write("10200" + '\t' + "0" + '\t' + "0" + '\t' + "10199" + '\t' + "10098" +
                              '\t' + "10099" + '\t' + "0" + '\t' + "0" + '\t' + "0" + '\t' +
                              str(datas[2]) + '\t' + str(datas[3]) + '\t' + str(datas[4]) + '\t' + str(datas[5]) + '\t' + str(datas[6]) + '\n')
            # 左边界
            elif (0<=int(datas[0])<=99) & (int(datas[1]) == 0):
                # f_write = open(path2, 'a')
                f_write.write(str(int(datas[0])+101*int(datas[1]))+ '\t'
                              +str(int(datas[0])+101*(int(datas[1])+1))+ '\t'
                              +str(int(datas[0])+101*(int(datas[1])+1)-1)+ '\t'
                              +str(int(datas[0])+101* int(datas[1])-1) + '\t'
                              + "0" +'\t'
                              + "0" + '\t'
                              + "0" + '\t'
                              +str(int(datas[0])+101* int(datas[1])+1) + '\t'
                              +str(int(datas[0])+101*(int(datas[1])+1)-1) + '\t'
                              +str(datas[2]) + '\t' + str(datas[3]) + '\t' + str(datas[4]) + '\t' + str(datas[5]) + '\t' + str(datas[6]) + '\n')

            # 上边界
            elif (int(datas[0]) == 0) & (1<=int(datas[1]) <= 99):
                # f_write = open(path2, 'a')
                f_write.write(str(int(datas[0])+101*int(datas[1])) + '\t'
                              +str(int(datas[0])+101*(int(datas[1])+1)) + '\t'
                              + "0" + '\t'
                              + "0" + '\t'
                              + "0" +'\t'
                              + str(int(datas[0])+101* (int(datas[1])-1)) + '\t'
                              + str(int(datas[0])+101* (int(datas[1])-1)+1) + '\t'
                              + str(int(datas[0])+101* int(datas[1]) + 1) + '\t'
                              + str(int(datas[0])+101* (int(datas[1])+1) + 1) + '\t'
                              + str(datas[2])+'\t'+str(datas[3])+'\t'+str(datas[4])+'\t'+str(datas[5])+'\t'+str(datas[6])+'\n')
            # 下边界
            elif (int(datas[0]) == 100) & (1 <= int(datas[1]) <= 99):
                # f_write = open(path2, 'a')
                f_write.write(str(int(datas[0])+101*int(datas[1]))+ '\t'
                              + str(int(datas[0])+101*(int(datas[1])+1)) + '\t'
                              + str(int(datas[0])+101* (int(datas[1])+1) - 1) + '\t'
                              + str(int(datas[0])+101* (int(datas[1])-1) - 1) + '\t'
                              + str(int(datas[0])+101* (int(datas[1])-1)) + '\t'
                              + "0" + '\t'
                              + "0" + '\t'
                              + "0" + '\t'
                              + str(int(datas[0])+101*(int(datas[1])+1)) + '\t'
                              + str(datas[2])+'\t'+str(datas[3])+'\t'+str(datas[4])+'\t'+str(datas[5])+'\t'+str(datas[6])+'\n')
            # 右边界
            elif ( 1<= int(datas[0]) <= 99) & (int(datas[1]) == 100):
                # f_write = open(path2, 'a')
                f_write.write(str(int(datas[0])+101*int(datas[1])) + '\t'
                              + "0" + '\t'
                              + "0" + '\t'
                              + "0" + '\t'
                              +  str(int(datas[0])+101* (int(datas[1])-1)) +'\t'
                              +  str(int(datas[0])+101* (int(datas[1])-1) - 1) + '\t'
                              +  str(int(datas[0])+101* (int(datas[1])-1)) + '\t'
                              +  str(int(datas[0])+101* (int(datas[1])-1) + 1) + '\t'
                              +  str(int(datas[0])+101* (int(datas[1])+1)) + '\t'
                              +  str(datas[2])+'\t'+str(datas[3])+'\t'+str(datas[4])+'\t'+str(datas[5])+'\t'+str(datas[6])+'\n')
            else:
                # f_write = open(path2, 'a')
                f_write.write(str(int(datas[0])+101*int(datas[1])) + '\t'
                              + str(int(datas[0])+101* (int(datas[1])+1))  + '\t'
                              + str(int(datas[0])+101* (int(datas[1])+1) - 1) + '\t'
                              + str(int(datas[0])+101* (int(datas[1])-1))  + '\t'
                              + str(int(datas[0])+101* (int(datas[1])-1) - 1)  + '\t'
                              + str(int(datas[0])+101* (int(datas[1])-1))  + '\t'
                              + str(int(datas[0])+101* (int(datas[1])-1) + 1)+ '\t'
                              + str(int(datas[0])+101* (int(datas[1])+1)) + '\t'
                              + str(int(datas[0])+101* (int(datas[1])+1) + 1) + '\t'
                              + str(datas[2])+'\t'+str(datas[3])+'\t'+str(datas[4])+'\t'+str(datas[5])+'\t'+str(datas[6])+'\n')



