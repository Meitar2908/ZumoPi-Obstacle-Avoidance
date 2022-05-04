import time
import cv2
import constants as const
import math

class move_info:
    def __init__(self):
        self.last_cords = {}
        self.speeds = {}
        self.robot_speed = (0,0)

    def find_speed(self,frame,distances):
        current_time = time.time()
        if("time" not in self.last_cords):
            self.last_cords["time"] = current_time
        dt = current_time - self.last_cords["time"]
        for dist in distances:
            i = dist[2]
            if(i not in self.last_cords):
                self.last_cords[i] = (dist[0],dist[1],dist[4])
            else:
                if(dt >= const.time_const_speed()):
                    delta_z = (dist[0] - self.last_cords[i][0])
                    delta_x = (dist[1] - self.last_cords[i][1])
                    centers_x = dist[4][0] - self.last_cords[i][2][0]
                    centers_y = dist[4][1] - self.last_cords[i][2][1]
                    if(delta_x == 0):
                        angle = 90
                    else:
                        angle = int(math.atan(delta_z/delta_x)*180/math.pi)
                    velocity_total = round(math.sqrt(delta_z**2+delta_x**2)/dt,1)
                    if(delta_z < 0 and delta_x <= 0
                    or delta_z >= 0 and delta_x < 0):
                        angle += 180
                    if(velocity_total <= 0.6 or (abs(centers_x) < 5 and abs(centers_y) < 5)):
                        velocity_total = 0
                        angle = 0
                    self.last_cords[i] = (dist[0],dist[1],dist[4])
                    self.speeds[i] = (velocity_total,angle%360)
                    # self.speeds[i] = (round(dist[0],1),round(dist[1],1))
        if(dt >= const.time_const_speed()):
            self.last_cords["time"]  = current_time
        self.show_and_calc_speed(frame,distances,frame.shape[1]/2)
        return frame

    def show_and_calc_speed(self,frame,distances,center_width):
        min = self.calc_speed(distances,center_width)
        for dist in distances:
            i = dist[2]
            # if(i in self.speeds):
            #     center = (dist[4][0]-int(0.2*dist[3]),dist[4][1]+int(1.5*dist[3]))
            #     text = "(" + str(self.speeds[i][0]) + "," + str(self.speeds[i][1]) + ")"
            #     if(i == min):
            #         cv2.putText(frame,text,center,cv2.FONT_HERSHEY_SIMPLEX,0.3,(255,0,0),1)
            #         # cv2.putText(frame,text,(center[0]-int(dist[3]),center[1]+int(1*dist[3])),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,255),3)
            #     else:
            #         cv2.putText(frame,text,center,cv2.FONT_HERSHEY_SIMPLEX,0.3,(0,0,255),1)
            #         # cv2.putText(frame,text,(center[0]-int(dist[3]),center[1]+int(1*dist[3])),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,255),3)


    def calc_speed(self,distances,center_width):
        min_value = -1
        min_index = 0
        for dist in distances:
            i = dist[2]
            if(i in self.speeds):
                if(min_value == -1 or abs(dist[4][0] - center_width) < abs(min_value - center_width)):
                    min_value = dist[4][0]
                    min_index = i     
        if(min_value == -1):
            self.robot_speed = (0,90)
        else:
            if(self.speeds[min_index][0] == 0):
                self.robot_speed = (0,90)
            else:
                self.robot_speed = (round(-self.speeds[min_index][0]*math.sin(self.speeds[min_index][1]),2),self.speeds[min_index][1]%180)
        return min_index