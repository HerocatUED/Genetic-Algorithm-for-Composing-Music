import numpy as np
from data.txt_to_vector import *
reference=np.array([69, 20, 72, 20, 72, 71, 69, 20, 69, 74, 74, 69, 74, 20, 20, 20, 
72, 20, 69, 20, 69, 71, 72, 20, 71, 72, 71, 67, 69, 20, 20, 20])  #需要取定一个参考乐曲

initial_parameter= [-0.1,-0.1,1,200,10,-100,-100,-100] #这些都是fitness function参数，之后可以人工修改

def evaluate_chord(chord):
    # chord是一个音符序列，假设为一个整数列表，表示和弦的音高
    
    # 在这里进行和弦的评估，根据具体需求和评估标准来编写评估逻辑
    
    # 示例评估逻辑：判断和弦是否符合某种特定的音程规则
    
    
    intervals = []  # 计算音程

    for i in range(31):
        if chord[i]!=0 and chord[i]!=20 and chord[i+1]!=0 and chord[i+1]!=20:
            intervals.append(chord[i+1] - chord[i])
    
    len_intervals=len(intervals) # 不计算休止和延音记号的，有效音程关系数量
    # 定义一个目标音程列表，例如：大三度、纯四度、纯五度
    target_intervals = [4, 5, 7]
    untarget_intervals=[1, 6, 8, 10] # 一些应该避免的音程
    
    # 计算和弦中与目标音程不符合的音程数量
    correct_intervals = sum([1 for interval in intervals if interval in target_intervals])
    incorrect_intervals = sum([1 for interval in intervals if interval in untarget_intervals])
    
    # 根据不符合音程的数量计算和弦的质量得分
    if len(intervals)==0:
        return 0
    
    chord_quality = 1 - (incorrect_intervals / len(intervals))+(correct_intervals / len(intervals))
    
    return 32*chord_quality/len_intervals # 按照音程数目标准化


def evaluate_leap_transitions(melody):
    leap_transitions = 0  # 记录跳跃音过渡的数量

    for i in range(len(melody) - 2):
        # 计算相邻音符之间的音高差
        count=0
        if melody[i]!=0 and melody[i]!=20 and melody[i+1]!=0 and melody[i+1]!=20:
            interval1 = abs(melody[i+1] - melody[i])
            interval2 = abs(melody[i+2] - melody[i+1])
            
            # 判断是否存在跳跃音过渡，例如大于一个预设的音程阈值
            leap_threshold = 7  # 音程阈值，例如4表示大三度
            if interval1 > leap_threshold and interval2 > leap_threshold:
                leap_transitions += 1
            
            count+=1
        
        else:
            continue
    
    if count==0:
        return 0
    
    leap_transition_fitness = 1 - (leap_transitions / count)  # 计算跳跃音过渡的质量得分
    
    return leap_transition_fitness

# 量化节奏
def rythme(chord):
    rythme=[]
    for i in range(len(chord)):
        time=1
        i+=1
        if 1==32:
            break

        while i<32 and chord[i]==20:
            time+=1
            i+=1
        rythme.append(time)
    return rythme




# 量化休止
def eval_rest(chord): 
    rest=[]
    for x in range(len(chord)):
        if chord[x]==0:
            rest.append(x)
    
    return rest


rest = []
ref=txt_to_vector()
for chord in ref:
    rest.append(eval_rest(ref))

def rest_reference():
    return rest



def fitness_function(x,parameter):  #x是自变量，其余是参数 
    part_1 = abs(np.mean(reference)-np.mean(x))  #part_1表示与参考数组的均值差距
    part_2 = abs(np.var(reference)-np.var(x))   #part_2表示与参考数组的方差差距
    part_3 = 0    #part_3表示超出一个范围的音符个数，这里取【65，75】
    n=0
    for i in range(len(x)):
        if not (65< x[i] <75) or (x[i] == 20) or (x[i] == 0):
            n += 1

    part_3 = 1/n
    part_4 = evaluate_chord(x) #part_4表示好听的和弦的比例
    part_5 = evaluate_leap_transitions (x)

    rythme_reference=rythme(reference)
    rythme_x=rythme(x)
    part_6 = abs(np.mean(rythme_reference)-np.mean(rythme_x))  #part_1表示与参考数组的均值差距
    part_7 = abs(np.var(rythme_reference)-np.var(rythme_x))

    
    part_8=abs(np.mean(rest_reference())-np.mean(eval_rest(x)))+abs(np.var(rest_reference())-np.var(eval_rest(x)))

    if x[0]==20:
        return -1000000 # 避免开始是延音记号
    
    return parameter[0]*part_1 + parameter[1]*part_2 + parameter[2]*part_3 + parameter[3]*part_4 + parameter[4]*part_5+parameter[5]*part_6 + parameter[6]*part_7+parameter[7]*part_8

#y=[64, 20, 20, 67, 67, 20, 20, 20, 64, 20, 20, 62, 60, 20, 20, 20, 62, 20, 20, 64, 67, 20, 20, 64, 62, 20, 20, 20, 20, 20, 20, 20]
#x = [64, 64, 64,64,64, 64, 64,64,64, 64, 64,64,64, 64, 62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62]
#random_y = np.random()
#print(fitness_function(y,initial_parameter))
