import math
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from matplotlib import pyplot as pb
import random
from datetime import datetime
import time
import csv
import sys
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

#!/usr/bin/env python
import os, sys, time
from ros2_network_analysis.msg import *
import std_msgs.msg
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
#from robot_msgs.msg import Robot_Pos

class recorder_rssi_odom(Node):

    msg_vec = WirelessLinkVector()
    odom_val = Odometry()
    vel = Twist()


    temp_step = 0
    temp_stamp_sec = 0
    temp_stamp_nsec = 0
    robot_pos_x = 0
    robot_pos_y = 0
    robot_odom_x = 0
    robot_odom_y = 0
    robot_odom_w = 0
    robot_q_x = 0
    robot_q_y = 0
    robot_q_z = 0
    robot_pos_w = 0
    robot_vel_x = 0
    robot_vel_y = 0
    robot_vel_w = 0
    vel_x = 0
    vel_y = 0
    vel_w = 0
    rssi1 = 0
    lqi1 = 0
    noise1 = 0
    status1 = False
    rssi2 = 0
    lqi2 = 0
    noise2 = 0
    status2 = False
    rssi3 = 0
    lqi3 = 0
    noise3 = 0
    status3 = False
    rssi4 = 0
    lqi4 = 0
    noise4 = 0
    status4 = False

    log_on_file = False
    now = datetime.now()

    def __init__(self):
        super().__init__('record_rssi_odom_node')

        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        self._local_seq = 0

        self.sub_rssi = self.create_subscription(WirelessLink, '/node1/network_analysis/wireless_quality', self.rssi1_callback, qos)
        self.sub_rssi = self.create_subscription(WirelessLink, '/node2/network_analysis/wireless_quality', self.rssi2_callback, qos)
        self.sub_rssi = self.create_subscription(WirelessLink, '/node3/network_analysis/wireless_quality', self.rssi3_callback, qos)
        self.sub_rssi = self.create_subscription(WirelessLink, '/node4/network_analysis/wireless_quality', self.rssi4_callback, qos)
        self.sub_odom = self.create_subscription(Odometry, '/odometry/filtered', self.odom_callback, qos)
        self.sub_vel = self.create_subscription(Twist, '/cmd_vel', self.vel_callback, qos)
        #self.sub_pos = self.create_subscription(Robot_Pos, '/positions', self.pos_callback, qos)

    def rssi1_callback(self, data):
        #self.msg_vec = data
        self._local_seq += 1
        self.temp_step = self._local_seq

        st = data.header.stamp
        self.temp_stamp_sec  = getattr(st, 'sec', 0)
        self.temp_stamp_nsec = getattr(st, 'nanosec', 0)
        self.rssi1 = data.rssi
        self.lqi1 = data.lqi
        self.noise1 = data.noise
        self.status1 = data.status
        self.log_on_file = True
        # print('true')
        if (self.log_on_file == True):
            string = "{:9d},".format(self.temp_step) +"{:11d},".format(self.temp_stamp_sec) +"{:11d},".format(self.temp_stamp_nsec)+ "{:10f},".format(self.robot_odom_x) + "{:10f},".format(self.robot_odom_y) +"{:10f},".format(self.robot_odom_w) + "{:10f},".format(self.robot_pos_x) + "{:10f},".format(self.robot_pos_y) +"{:10f},".format(self.robot_pos_w) + "{:10f},".format(self.vel_x) + "{:10f},".format(self.vel_y) + "{:10f},".format(self.vel_w) + "{:5f},".format(self.rssi1) + "{:5f},".format(self.lqi1) + "{:5f},".format(self.noise1) + "{:2d},".format(self.status1) + "{:5f},".format(self.rssi2) + "{:5f},".format(self.lqi2) + "{:5f},".format(self.noise2) + "{:2d},".format(self.status2) + "{:5f},".format(self.rssi3) + "{:5f},".format(self.lqi3) + "{:5f},".format(self.noise3) + "{:2d},".format(self.status3) + "{:5f},".format(self.rssi4) + "{:5f},".format(self.lqi4) + "{:5f},".format(self.noise4) + "{:2d}".format(self.status4) + "\n"
        # self.file_log.write (string)
    
        
    def rssi2_callback(self, data):
        #self.msg_vec = data
        self.rssi2 = data.rssi
        self.lqi2 = data.lqi
        self.noise2 = data.noise
        self.status2 = data.status

    def rssi3_callback(self, data):
        #self.msg_vec = data
        self.rssi3 = data.rssi
        self.lqi3 = data.lqi
        self.noise3 = data.noise
        self.status3 = data.status

    def rssi4_callback(self, data):
        #self.msg_vec = data
        self.rssi4 = data.rssi
        self.lqi4 = data.lqi
        self.noise4 = data.noise
        self.status4 = data.status

    def odom_callback(self,data):
        #self.odom_val = data
        self.robot_odom_x = data.pose.pose.position.x
        self.robot_odom_y = data.pose.pose.position.y
        # self.robot_q_x = data.pose.pose.orientation.x
        # self.robot_q_y = data.pose.pose.orientation.y
        # self.robot_q_z = data.pose.pose.orientation.z
        self.robot_odom_w = data.pose.pose.orientation.w
        # self.robot_vel_x = data.twist.twist.linear.x 
        # self.robot_vel_y = data.twist.twist.linear.y
        # self.robot_vel_w = data.twist.twist.angular.z
        self.robot_pos_x = self.robot_odom_x
        self.robot_pos_y = self.robot_odom_y
        self.robot_pos_w = self.robot_odom_w
        
    def pos_callback(self,data):
        if data.robot_pos:
            self.robot_pos_x = data.robot_pos[0].pose.pose.position.x
            self.robot_pos_y = data.robot_pos[0].pose.pose.position.y
            # self.robot_q_x = data.pose.pose.orientation.x
            # self.robot_q_y = data.pose.pose.orientation.y
            # self.robot_q_z = data.pose.pose.orientation.z
            self.robot_pos_w = data.robot_pos[0].pose.pose.orientation.w
            # self.robot_vel_x = data.twist.twist.linear.x 
            # self.robot_vel_y = data.twist.twist.linear.y
            # self.robot_vel_w = data.twist.twist.angular.z

    def vel_callback(self,data):
        self.vel_x = data.linear.x
        self.vel_y = data.linear.y
        self.vel_w = data.angular.z

    def function_init(self):
        if (self.log_on_file == True):
            string ="temp_step,temp_sec,temp_nsec,robot_odom_x,robot_odom_y,robot_odom_w,robot_pos_x,robot_pos_y,robot_pos_w,vel_x,vel_y,vel_w,rssi1,lqi1,noise1,status1,rssi2,lqi2,noise2,status2,rssi3,lqi3,noise3,status3,rssi4,lqi4,noise4,status4\n"
        # self.file_log.write (string)


# pos= (4,7)
# pos = (1,14)
# Next Pos(-5,-1)
#freq GHz
#power in decibels per milliwatt (dBm)

def quaternion_to_yaw(x, y, w, z):
        t0 = 2.0 * (w * z + x * y)
        t1 = 1.0 - 2.0 * (y * y + z * z)
        yaw = math.atan2(t0, t1)
        return yaw

DT = 0.1
def motion_model(x,u):
    F = np.array([[1.0, 0, 0],
                  [0, 1.0, 0],
                  [0, 0, 1.0]])

    B = np.array([[DT * math.cos(x[2]), 0],
                  [DT * math.sin(x[2]), 0],
                  [0.0, DT]])

    xd = F.dot(x) + B.dot(u)

    return xd

def dist(x, y, pos):
    return math.sqrt((pos[0]-x)**2 + (pos[1]-y)**2)


rss0 = 20 * math.log10(3 / (4 * math.pi * 2.4 * 10))
rss0 = rss0-2*random.random()
print(rss0)
#areaSize=(2.34, 1.75)
areaSize=(3.048, 3.96)


#node_pos=[(0,0),(0,1.75),(2.34,1.75),(2.34,0)]
node_pos=[(0,0),(0,3.048),(3.96,3.048),(3.96, 0)]

def gen_wifi(freq=2.4, power=20, trans_gain=0, recv_gain=0, size=areaSize, pos=(5,5), shadow_dev=2, n=3,noise=2):
    if pos is None:
        pos = (random.randrange(size[0]), random.randrange(size[1]))

    random.seed(datetime.now())
    
    normal_dist = np.random.normal(0, shadow_dev, size=[int(size[0])+1, int(size[1])+1])
    rss = []

    random.seed(datetime.now())

    for x in range(0,4):
        ix = int(np.clip(pos[0], 0, int(size[0])))
        iy = int(np.clip(pos[1], 0, int(size[1])))
        distance = dist(node_pos[x][0], node_pos[x][1], pos)
        val = rss0 - 10 * n * math.log10(distance) + normal_dist[ix][iy] if distance != 0 else rss0 + normal_dist[ix][iy]
        rss.append(val-noise*random.random())
        # print("rssi: "+str(val)+"\tnode_position: "+str(node_pos[x])+"\tPF_Pos: "+str(pos)+"\tdistance: "+str(distance)+"\t"+str(normal_dist[int(pos[0])][int(pos[1])]))
    return rss

doa=[]
def find_doa(overall_rss,original_tragectory,i):
    inner_curr = i
    limit = i-100 if i>100 else 0
    est_sin_sum = 0
    est_cos_sum = 0
    starting_curr = inner_curr
    weight_sum = 0
    # average estimated DoA calculated
    while inner_curr >= limit:
    # print(str(overall_rss[i]))
        gy = ((overall_rss[i][1]-overall_rss[i][0])/2) + ((overall_rss[i][2]-overall_rss[i][3])/2)
        gx = ((overall_rss[i][2]-overall_rss[i][1])/2) + ((overall_rss[i][3]-overall_rss[i][0])/2)
        estimated_grad=np.arctan(gy/gx) if gx!=0 else 0
        quat = quaternion_to_yaw(original_tragectory[i][0],original_tragectory[i][1], original_tragectory[i][2],original_tragectory[i][3])
        estimated_grad += quat
        if estimated_grad > math.pi:
            estimated_grad = -2 * math.pi + estimated_grad
        elif estimated_grad < -math.pi:
            estimated_grad = math.pi - abs(-math.pi - estimated_grad)
        weight = 0.99 ** (inner_curr - starting_curr)
        weight_sum += weight
        estimated_grad = weight * estimated_grad
        est_sin_sum += math.sin(estimated_grad)
        est_cos_sum += math.cos(estimated_grad)
        inner_curr -= 1
    avg_est_sin = est_sin_sum / weight_sum
    avg_est_cos = est_cos_sum / weight_sum
    avg_grad = math.atan2(avg_est_sin, avg_est_cos)
    doa.append(avg_grad)
    # if not prev:
    #     prev = (i,avg_grad)
    return avg_grad



def localize(rec, run_tag):

    initial_pos=(0.05,0.05)
    possible_x = list(np.arange(0.9,1.3,0.05))
    possible_y = list(np.arange(0.6,1,0.05))
    # possible_x = list(np.arange(0.0, areaSize[0] + 0.001, 0.05))
    # possible_y = list(np.arange(0.0, areaSize[1] + 0.001, 0.05))
    num_particles = 1000

    overall_rss=[]
    original_tragectory=[]
    velocity=[]
    Previous_pos = initial_pos


    plt.ion()

    random.seed(datetime.now())
    previous_errors =[]
    distance_error =[]
    particles = []
    times = []
    Previous_pos = initial_pos
    start_time = time.time()
    for x in range(num_particles):
        particles.append((random.choice(possible_x),random.choice(possible_y)))
    fig, plt_pos = plt.subplots(1,1)
    plt_pos.set_title("Localization")
    # plt_pos.set_xlim((-0.25,areaSize[0]+0.25))
    # plt_pos.set_ylim((-0.25,areaSize[1]+0.25))
    plt_pos.set_xlim((-10, 15))
    plt_pos.set_ylim((-10, 15))
    #plt_pos.set_xlim((-0.25,areaSize[0]+0.25))
    #plt_pos.set_ylim((-0.25,areaSize[1]+0.25))

    #plt_pos.relim(); plt_pos.autoscale_view()
    i = 0
    legend_added = False
    try:
        while rclpy.ok():
            try:
                rclpy.spin_once(rec, timeout_sec=0.05)
            except Exception as exc:
                if 'context is not valid' in str(exc):
                    break
                raise

            if rec.log_on_file == True:
                rec.log_on_file = False
                x, y, w, z = rec.robot_pos_x, rec.robot_pos_y, rec.robot_pos_w, 0
                original_tragectory.append((x,y,w,z))
                rss =  [rec.rssi1,rec.rssi2,rec.rssi3,rec.rssi4]
                overall_rss.append(rss)
                velocity.append([rec.vel_x,rec.vel_w])
                positions =[]
                errors=[]
                weights =[]
                actual_rss_ls=[]
                error=0
                for particle in particles:
                    x,y=particle[0],particle[1]
                    actual_rss = gen_wifi(pos=(x,y),noise=0)
                    gy = ((actual_rss[1]-actual_rss[0])/2) + ((actual_rss[2]-actual_rss[3])/2)
                    gx = ((actual_rss[2]-actual_rss[1])/2) + ((actual_rss[3]-actual_rss[0])/2)
                    adoa=np.arctan(gy/gx) if gx !=0 else 0
                    avg_doa=find_doa(overall_rss,original_tragectory,i)
                    error=abs(adoa-avg_doa)

                    std_error=np.std(np.subtract(actual_rss,overall_rss[i]))
                    omega=((1/((std_error)*math.sqrt(2*math.pi)))*(math.pow(math.e,-(math.pow(error,2)/(2*(std_error**2))))))
                    for i in range(len(previous_errors)-1,len(previous_errors)-4 if len(previous_errors) > 5 else 0,-1):
                        omega=omega*((1/((std_error)*math.sqrt(2*math.pi)))*(math.pow(math.e,-(math.pow(previous_errors[i],2)/(2*(std_error**2))))))

                    weights.append(omega)
                    positions.append((x,y,))
                    errors.append(error)
                    actual_rss_ls.append(actual_rss)

                sum_weight=np.sum(weights)
                if sum_weight != 0:
                    for j in range(0,len(weights)):
                        weights[j]=weights[j]/sum_weight

                max_weight = max(weights)
                max_index = weights.index(max_weight)
                pos = positions[max_index]
                pos = ((pos[0]+original_tragectory[i][0])/2,(pos[1]+original_tragectory[i][1])/2)
                previous_errors.append(errors[max_index])
                distance_error.append(dist(pos[0],pos[1],original_tragectory[i]))

                pos_x = [pos[0],pos[1],original_tragectory[i][2]]
                xd = motion_model(pos_x,velocity[i])

                num_particles=math.ceil(num_particles/2) if num_particles/2>200 else 200
                particles=[]
                for x in range(num_particles):
                    particles.append((random.uniform(pos_x[0]-0.1 if pos_x[0]-0.1 >=-areaSize[0] else -areaSize[0], pos_x[0]+0.1 if pos_x[0]+0.1 <=areaSize[0] else areaSize[0])
                    ,random.uniform(pos[1]-0.1 if pos_x[1]-0.1 >=-areaSize[1] else -areaSize[1], pos_x[1]+0.1 if pos_x[1]+0.1 <=areaSize[1] else areaSize[1])))
                if i>0:
                    gt_label = 'Ground truth' if not legend_added else '_nolegend_'
                    est_label = 'Estimated trajectory' if not legend_added else '_nolegend_'
                    plt_pos.plot([original_tragectory[i-1][0],original_tragectory[i][0]],[original_tragectory[i-1][1],original_tragectory[i][1]],'g-',linewidth=2.4,clip_on=False,label=gt_label)
                    plt_pos.plot([Previous_pos[0],pos[0]],[Previous_pos[1],pos[1]],'r-',linewidth=2,clip_on=False,label=est_label)
                    if not legend_added:
                        plt_pos.legend(loc='upper right')
                        legend_added = True

                plt.draw()
                plt.pause(0.0001)
                Previous_pos = pos
                i+=1
    except KeyboardInterrupt:
        pass
    finally:
        plt.show(block=False)
        output_file = 'predicted_trajectory_' + run_tag + '.png'
        fig.savefig(output_file)
        print('Saved trajectory figure:', output_file)
        print("--- Computation Time: %s seconds ---" % (time.time() - start_time))
        if previous_errors and distance_error:
            rsscumulativeEror=np.sum(previous_errors)
            rssmeanError=np.average(previous_errors)
            rssStandardDeviationError=np.std(previous_errors)
            distcumulativeEror=np.sum(distance_error)
            distmeanError=np.average(distance_error)
            distStandardDeviationError=np.std(distance_error)
            print("RSS_ERROR:   Cumulative Error: " + str(rsscumulativeEror)+"\tMean  Error: "+str(rssmeanError)+"\tStandard Deviation: "+str(rssStandardDeviationError))
            print("DIST_ERROR:   Cumulative Error: " + str(distcumulativeEror)+"\tMean  Error: "+str(distmeanError)+"\tStandard Deviation: " + str(distStandardDeviationError))
        plt.close(fig)


def main(argv=None):
    rclpy.init(args=argv)
    rec = recorder_rssi_odom()
    run_tag = argv[1] if argv is not None and len(argv) > 1 else datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    try:
        localize(rec, run_tag)
    except KeyboardInterrupt:
        plt.savefig('predicted_trajectory_' + run_tag + '.png')
        pass
    rec.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main(sys.argv)
