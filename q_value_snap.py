import math
from collections import Counter
import sys


#convert input string to list.
def str2list(input_str):
   return input_str.split()


#calculate 3D angle of target point set.
def ang(x,y,z):
   vec_1=list(map(lambda i,j: i-j, x,y))
   vec_2=list(map(lambda i,j: i-j, z,y))
   ans=sum(map(lambda x,y: x*y,vec_1,vec_2))/(math.sqrt(sum(map(lambda x:x*x,vec_1)))*math.sqrt(sum(map(lambda y:y*y,vec_2))))
   return abs(math.acos(ans)*180/math.pi)


#calculate 3D distance of given point set.
def dis(x,y):
   return math.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2+(x[2]-y[2])**2)


#number of hbonds among two particular residues
def num_hbond(res_1,res_2,dis_cut,ang_cut):
    ans=0
    if (dis(res_1.n,res_2.o)<=dis_cut and ang(res_1.n,res_1.h,res_2.o)>=ang_cut) or (dis(res_2.n,res_1.o)<=dis_cut and ang(res_2.n,res_2.h,res_1.o)>=ang_cut):
        ans=1
    return ans


#x-mo,y-fi
def get_q_value(data_in,dis_cut,ang_cut,res_num):
    tmp = [[0 for m in range(res_num)] for n in range(res_num)]
    fi_list=data_in[:740]
    mo_list=data_in[740:]
    print("mo",len(mo_list))
    for fi in range(len(fi_list)):
        for mo in range(len(mo_list)):
            res_1=residue(fi_list[fi][0],fi_list[fi][1],fi_list[fi][2],fi_list[fi][3])
            res_2=residue(mo_list[mo][0]%37,mo_list[mo][1],mo_list[mo][2],mo_list[mo][3])

            tmp[(fi%37)-1][mo]+=num_hbond(res_1,res_2,dis_cut,ang_cut)
    return tmp


#def count_hbond(res_1,res_2,dis_cut,ang_cut):
#    if is_hbond(res_1,res_2,dis_cut,ang_cut):
#        return


class residue:
    def __init__(self, res_index, n_pos,o_pos,h_pos):
        self.index = res_index
        self.n = n_pos
        self.h = h_pos
        self.o = o_pos


def file_snaps(file,key_word):
    line=file.readline()
    mark=0
    while line:
        if str2list(line)[0]==key_word:
            mark+=1
        line=file.readline()
    return mark

def cal_q_value(matrix_in,eff_range):
    ans=0
    tmp=0
    for i in range(len(matrix_in)):
        for j in range(i-eff_range,i+eff_range+1):
            try:
                tmp+=matrix_in[i][j]
            except IndexError:
                continue
        if tmp>0:
            ans+=1
        tmp=0
    return ans/len(matrix_in)


#setup
dis_cut=3.5
ang_cut=120
res_num=37
eff_range=2


#ans=[[0 for x in range(res_num)] for y in range(res_num)]

#snap_count=file_snaps(f,"ENDMDL")
snap_mark=0
chain_mark=0

cur_snap=[]

#for each snap within "ENDMDL"
#读取数据，储存至两个数组，fi和mo

data_in=[]
cur_data=[]
q_list=[]
i=0

f=open("100steps.pdb")
line=f.readline()
while line:
    cur_list=str2list(line)
    if cur_list[0]=="TER":
        line=f.readline()
        continue
    if cur_list[0]=="ENDMDL":
        snap_mark+=1
        print(snap_mark)
        tmp=get_q_value(data_in,dis_cut,ang_cut,res_num)
        out_q=cal_q_value(tmp,eff_range)
        q_list.append(out_q)
        data_in=[]


    else:
        if cur_list[2] == "N":
            cur_data.append(int(cur_list[5]))
            cur_data.append(list(map(float, cur_list[6:9])))
        if cur_list[2] == "O":
            cur_data.append(list(map(float, cur_list[6:9])))
        if cur_list[2] == "HN":
            cur_data.append(list(map(float, cur_list[6:9])))
            data_in.append(cur_data)
            cur_data = []
    line = f.readline()

#print(ans)
f.close()
res=0



f=open("q_snap.dat","w+")
for i in range(len(q_list)):

    f.write(str(q_list[i]))
    f.write("\n")
f.write("max:")
f.write("\t")
f.write(str(max(q_list)))

f.close()