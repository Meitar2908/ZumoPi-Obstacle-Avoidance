import constants as const

class file_buffers:
    def __init__(self,write_data_to_file):
        self.write_data_to_file = write_data_to_file
        self.frame_counter = 0
        self.original_angles_buffer = []
        self.force_buffer = []
        self.angles_buffer = []
        self.x_buffer = []
        self.z_buffer = []
        self.radius_buffer =[]
        self.speed_size_buffer = []
        self.speed_angle_buffer = []

    def save_angle(self,angle):
        if(self.write_data_to_file):
            self.original_angles_buffer.append(str(angle))

    def write_to_files(self,zumoAngle,zumoSpeed,distances,speed):
        if(self.write_data_to_file):
            ball_found = False
            self.frame_counter += 1
            for dist in distances:
                if(dist[2] == const.color):
                    ball_found = True
                    self.z_buffer.append(str(dist[0]))
                    self.x_buffer.append(str(dist[1]))
                    self.radius_buffer.append(str(dist[3]))
                    self.force_buffer.append(str(zumoSpeed))
                    self.angles_buffer.append(str(zumoAngle))
                    self.speed_angle_buffer.append(str(speed[1]))
                    self.speed_size_buffer.append(str(speed[0]))
            if(not ball_found):
                self.z_buffer.append(' ')
                self.x_buffer.append(' ')
                self.radius_buffer.append(' ')
                self.force_buffer.append(str(zumoSpeed))
                self.angles_buffer.append(str(zumoAngle))
                self.speed_angle_buffer.append(str(speed[1]))
                self.speed_size_buffer.append(str(speed[0]))
            if(self.frame_counter == 360):
                self.write()
                

    def write(self):
        with open('/home/pi/WS_Zumo/ZumoObstacles/data_files/angles.txt','w') as file:
            file.write('\n'.join(self.angles_buffer))
        with open('/home/pi/WS_Zumo/ZumoObstacles/data_files/forces.txt','w') as file:
            file.write('\n'.join(self.force_buffer))
        with open('/home/pi/WS_Zumo/ZumoObstacles/data_files/distance_x.txt','w') as file:
            file.write('\n'.join(self.x_buffer))
        with open('/home/pi/WS_Zumo/ZumoObstacles/data_files/distance_z.txt','w') as file:
            file.write('\n'.join(self.z_buffer))
        with open('/home/pi/WS_Zumo/ZumoObstacles/data_files/radius.txt','w') as file:
            file.write('\n'.join(self.radius_buffer))
        with open('/home/pi/WS_Zumo/ZumoObstacles/data_files/speed_angles.txt','w') as file:
            file.write('\n'.join(self.speed_angle_buffer))
        with open('/home/pi/WS_Zumo/ZumoObstacles/data_files/speed_size.txt','w') as file:
            file.write('\n'.join(self.speed_size_buffer))
        with open('/home/pi/WS_Zumo/ZumoObstacles/data_files/original_angles.txt','w') as file:
            file.write('\n'.join(self.original_angles_buffer))
        self.frame_counter = 0
        self.force_buffer = []
        self.angles_buffer = []
        self.x_buffer = []
        self.z_buffer = []
        self.radius_buffer =[]
        self.speed_size_buffer = []
        self.speed_angle_buffer = []
        self.write_data_to_file = False
        print("wrote to files!")