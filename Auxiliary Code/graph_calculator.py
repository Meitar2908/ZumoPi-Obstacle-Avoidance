
from cProfile import label
import matplotlib.pyplot as plt
from numpy import angle


def read_files(text):
    angles_f = open("data files/"+text+"angles.txt", 'r')
    dist_x_f = open("data files/"+text+"distance_x.txt", 'r')
    dist_z_f = open("data files/"+text+"distance_z.txt", 'r')
    forces_f = open("data files/"+text+"forces.txt", 'r')
    og_angles_f = open("data files/"+text+"original_angles.txt", 'r')
    radius_f = open("data files/"+text+"radius.txt", 'r')
    speed_angles_f = open("data files/"+text+"speed_angles.txt", 'r')
    speed_size_f = open("data files/"+text+"speed_size.txt", 'r')
    weights = []
    if(text == "weight_exp_"):
        weights_f = open("data files/"+text+"weights.txt", 'r')
        weights = list(map(float, weights_f.readlines()))
        weights_f.close()
    angles = list(map(float, angles_f.readlines()))
    dist_x = list(map(float, dist_x_f.readlines()))
    dist_z = list(map(float, dist_z_f.readlines()))
    forces = list(map(float, forces_f.readlines()))
    og_angles = list(map(float, og_angles_f.readlines()))
    radius = list(map(float, radius_f.readlines()))
    speed_angles = list(map(float, speed_angles_f.readlines()))
    speed_size = list(map(float, speed_size_f.readlines()))
    angles_f.close()
    dist_x_f.close()
    dist_z_f.close()
    forces_f.close()
    og_angles_f.close()
    radius_f.close()
    speed_angles_f.close()
    speed_size_f.close()
    return (angles, dist_x, dist_z, forces, og_angles, radius, speed_angles, speed_size, weights)

def list_op(list1, list2, op=0):
    new_list = list1.copy()
    if(isinstance(list2,int)):
        temp = list2
        list2 = []
        for i in range(len(list1)):
            list2.append(temp)
    if(op == 0):
        for i in range(len(list1)):
            new_list[i] = list1[i] + list2[i]
    if(op == 1):
        for i in range(len(list1)):
            new_list[i] = list1[i] - list2[i]
            if(new_list[i] >= 2):
                new_list[i] -= 1
            elif(new_list[i] <= -2):
                new_list[i] += 1
    if(op == 2):
        for i in range(len(list1)):
            new_list[i] = list1[i] * list2[i]
    if(op == 3):
        for i in range(len(list1)):
            if(list2[i] != 0):
                new_list[i] = list1[i] / list2[i]
    return new_list

def offset(list, offset, minus = 1):
    control_copy = list.copy()
    for i in range(360):
        if(i < offset):
            list[i] = 0
        else:
            list[i] = minus * control_copy[i - offset]

def angle_interference_graph():
    text = "one_blue_ball_"
    angles_blue, dist_x, dist_z, forces, og_angles_blue, radius, speed_angles, speed_size, weights = read_files(text)
    text = "one_red_ball_"
    angles_red, dist_x, dist_z, forces, og_angles_red, radius, speed_angles, speed_size, weights = read_files(text)
    text = "one_green_ball_"
    angles_green, dist_x, dist_z, forces, og_angles_green, radius, speed_angles, speed_size, weights = read_files(text)
    text = "one_yellow_ball_"
    angles_yellow, dist_x, dist_z, forces, og_angles_yellow, radius, speed_angles, speed_size, weights = read_files(text)
    control_angles_blue = list_op(angles_blue, og_angles_blue, 1)
    control_angles_red = list_op(angles_red, og_angles_red, 1)
    control_angles_green = list_op(angles_green, og_angles_green, 1)
    control_angles_yellow = list_op(angles_yellow, og_angles_yellow, 1)
    offset(control_angles_yellow, 70,-1)
    offset(control_angles_red, 0,-1)
    offset(control_angles_blue, 80,-1)
    offset(control_angles_green, 150,-1)
    black = []
    time = []
    for i in range(360):
        black.append(0)
        time.append(i/17.9)
    plt.plot()
    plt.plot(time,control_angles_red, linestyle='-', label="red ball", color="r")
    plt.plot(time,control_angles_yellow, linestyle='-', label="yellow ball", color="y")
    plt.plot(time,control_angles_blue, linestyle='-', label="blue ball", color="b")
    plt.plot(time,control_angles_green, linestyle='-', label="green ball", color="g")
    plt.plot(time,black, color="0.3")
    plt.title("Angle interference as a function of time")
    plt.ylabel('angle [degree]')
    plt.xlabel('time [sec]')
    plt.grid()
    plt.legend()
    plt.show()

def distances_graph(ZorX = 1):
    if(ZorX == 1):
        text = "distance_exp_"
        angles, dist_x, dist_z, forces, og_angles, radius, speed_angles, speed_size, weights = read_files(text)
        dist = []
        yisx = []
        for i in range(260):
            dist.append(30-0.0833*i)
        for i in range(7,31):
            yisx.append(i)
        dist_diff = list_op(dist_z[100:360], dist, 1)
        # dist_diff = list_op(dist_diff, dist,3)
        # dist_diff = list_op(dist_diff,100,2)
        plt.plot(dist, dist_diff, linestyle='-',
                 label="Calculated_Z(Real Z)")
        plt.title("Calculated Z distance error as a function of Real Z distance")
        plt.ylabel('Calculated Z Error [cm]')
        # plt.plot(dist,dist_z[100:360],linestyle = '-',label = "Calculated_Z(Real Z)")
        # plt.plot(yisx, yisx, linestyle='--', label="Calculated Z = Real Z")
        # plt.title("Calculated Z distance as a function of Real Z distance")
        # plt.ylabel('Calculated Z [cm]')
        plt.xlabel('Real Z [cm]')
        plt.grid()
        # plt.legend()
        plt.show()
    else:
        text = "distance_x_exp"
        angles, dist_x, dist_z, forces, og_angles, radius, speed_angles, speed_size, weights = read_files(text)
        dist = []
        yisx = []
        for i in range(180):
            dist.append(-15+0.18*i)
        for i in range(-15, 16):
            yisx.append(i)
        dist_diff = list_op(dist_x[25:205], dist, 1)
        plt.plot(dist, dist_diff, linestyle='-', label="Calculated_X(Real X)")
        # plt.plot(yisx, yisx, linestyle='--', label="Calculated X = Real X")
        plt.title("Calculated X distance error as a function of Real X distance")
        plt.ylabel('Calculated X Error [cm]')
        plt.xlabel('Real X [cm]')
        plt.grid()
        # plt.legend()
        plt.show()

def manual_vs_control():
    text = "one_blue_ball_"
    angles_blue, dist_x, dist_z, forces, og_angles_blue, radius, speed_angles, speed_size, weights = read_files(
        text)
    for i in range(207):
        angles_blue[i+153] = 0
        og_angles_blue[i+153] = 0
    text = "one_red_ball_"
    angles_red, dist_x, dist_z, forces, og_angles_red, radius, speed_angles, speed_size, weights = read_files(
        text)
    for i in range(276):
        angles_red[i+84] = 0
        og_angles_red[i+84] = 0
    text = "one_green_ball_"
    angles_green, dist_x, dist_z, forces, og_angles_green, radius, speed_angles, speed_size, weights = read_files(
        text)
    text = "one_yellow_ball_"
    angles_yellow, dist_x, dist_z, forces, og_angles_yellow, radius, speed_angles, speed_size, weights = read_files(
        text)
    for i in range(265):
        angles_yellow[i+95] = 0
        og_angles_yellow[i+95] = 0
    offset(angles_yellow, 70)
    offset(og_angles_yellow, 70)
    offset(angles_red, 0)
    offset(angles_blue, 80)
    offset(og_angles_blue, 80)
    offset(angles_green, 150)
    offset(og_angles_green, 150)
    black = []
    time = []
    for i in range(360):
        black.append(0)
        time.append(i/17.9)
    # plt.plot(time, angles_red, linestyle='--',
    #          label="controlled angle red ball", color="r")
    # plt.plot(time, og_angles_red, linestyle='-', color="r")
    # plt.plot(time, angles_yellow, linestyle='--',
    #          label="controlled angle yellow ball", color="y")
    # plt.plot(time, og_angles_yellow, linestyle='-', color="y")
    # plt.plot(time, angles_blue, linestyle='--',
    #          label="controlled angle blue ball", color="b")
    # plt.plot(time, og_angles_blue, linestyle='-', color="b")
    # plt.plot(time, angles_green, linestyle='--',
    #          label="controlled angle green ball", color="g")
    # plt.plot(time, og_angles_green, linestyle='-', color="g")
    # plt.plot(time, black, color="0.3")
    plt.plot(time, angles_red, linestyle='--',
                  color="r")
    plt.plot(time, og_angles_red, linestyle='-', color="r")
    plt.plot(time, angles_yellow, linestyle='--',
              color="y")
    plt.plot(time, og_angles_yellow, linestyle='-', color="y")
    plt.plot(time, angles_blue, linestyle='--',
              color="b")
    plt.plot(time, og_angles_blue, linestyle='-', color="b")
    plt.plot(time, angles_green, linestyle='--',
              color="g")
    plt.plot(time, og_angles_green, linestyle='-', color="g")
    plt.plot(time, black, color="0.3")
    plt.plot([], label="manual angles", linestyle='-', color="k")
    plt.plot([],label = "controlled angles",linestyle = '--',color = "k")
    plt.title("manual angle and controlled angle as a function of time")
    plt.ylabel('angle [degree]')
    plt.xlabel('time [sec]')
    plt.grid()
    plt.legend()
    plt.show()


def weight_func(alpha = 1.6,beta = 20):
    weight = []
    z = []
    for i in range (1000):
        z.append(0.1*i-20)
        weight.append(1/(1+alpha**(((0.1*i)-20)-beta)))
    plt.plot(z, weight, linestyle='-')
    plt.title("Boundaries weight as a function of Z")
    plt.ylabel("weight")
    plt.xlabel("Z [cm]")
    plt.show()


# angle_interference_graph()

# distances_graph(2)

# distances_graph(0)

# manual_vs_control()

weight_func()

