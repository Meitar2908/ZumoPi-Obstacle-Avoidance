import constants as const
import cv2
import math
import imutils
import data_files as files
import move_info as move

data = files.file_buffers(const.write_to_files)
movements = move.move_info()

def auto_drive(img,zumoSpeed,zumoAngle,is_manual,frame_kind):
    #initialize the values to 0
    if(zumoAngle == None):
        zumoAngle = 0
    if(zumoSpeed == None):
        zumoSpeed = 0
    #check if the frame is valid
    if(img is None):
        return (zumoSpeed, zumoAngle, img, movements.robot_speed)
    #start
    fixed_frame = fix_img(img)
    distances , objects_frame = find_objects(fixed_frame)
    data.save_angle(zumoAngle)
    if(not is_manual):
        zumoSpeed , zumoAngle = control(distances,zumoSpeed,zumoAngle)
    text_and_objects_frame = movements.find_speed(objects_frame,distances)
    data.write_to_files(zumoAngle,zumoSpeed,distances,movements.robot_speed)
    if(frame_kind):
        return (zumoSpeed, zumoAngle, text_and_objects_frame, movements.robot_speed)
    return (zumoSpeed, zumoAngle, img, movements.robot_speed)

def fix_img(img):
    h,  w = img.shape[:2]
    mapx, mapy = cv2.initUndistortRectifyMap(const.matrix(), const.dist(), None, const.matrix(), (w, h), 5)
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
    x ,y, w, h = (20, 25, 300, 215)
    return dst[x:h,y:w]
    # return dst

def find_objects(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #             red              blue        green         yellow
    Lower = [(0, 104, 104),   (95, 229, 62), (64, 158, 73), (23, 100, 97)]
    Upper = [(20, 255, 255), (113, 255, 219), (92, 255, 204), (42, 255, 227)]
    distances = []
    for i in range(0, len(Lower)):
        #create binary mask of the objects
        mask = cv2.inRange(img, Lower[i], Upper[i])

        #red's hue bounderies are between 178 - 20 (hue cycles every 180)
        if(i == 0):
            Lower_cycle = (172,104,113)
            Upper_cycle = (180,255,255)
            mask += cv2.inRange(img, Lower_cycle,Upper_cycle)

        #clean 'bubbles' in the picture
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
    	# find contours in the mask
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            center = (int(x), int(y))
            # only proceed if the radius meets a minimum size
            if radius > 8:
                cv2.circle(img, center, int(radius),(0, 255, 255), 2)
                cv2.circle(img, center, math.ceil(radius/10), (0, 0, 255), -1)  
                # calculates the distance and angle
                distance = (const.ball_radius()*const.focal())/radius
                ratio = const.height()/distance
                if(ratio > 1):
                    ratio = 1
                teta = math.acos(ratio)
                distance_z = distance*math.sin(teta)
                distance_x = ((x-img.shape[1]*0.5)/radius)*const.ball_radius()
                distances.append((distance_z,distance_x,i,radius,center))   
                #sampeling the data
    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    return (distances,img)

def calc_move_vectors(last_cords,distances):
    vectors = [0,0,0,0]
    for distance in distances:
        i = distance[2]
        if(last_cords[i] == [-1,-1]):
            last_cords[i][0] = distance[0]
            last_cords[i][1] = distance[1]
        else:
            vectors[0] = (math.sqrt())

def control(distances,zumospeed,zumoangle):
    #find boundaries
    bounderies = get_forbidden_boundaries(distances)
    for i in range(len(bounderies)):
        weight = const.weight(distances[i][0])
        bound_left = bounderies[i][0]
        bound_right = bounderies[i][1]
        if(bound_left == 180 and bound_right == 0):
            zumospeed *= 1.5
        if(zumoangle >= bound_left and zumoangle <= bound_right
        or zumoangle <= bound_left and zumoangle >= bound_right):
            if(distances[i][1] >= 0):
                zumoangle = bound_left*weight + zumoangle*(1-weight)
            else:
                zumoangle = bound_right*weight + zumoangle*(1-weight)
    return (zumospeed,zumoangle)

def get_forbidden_boundaries(distances):
    bounderies = []
    for object in distances:
        weight = const.weight(object[0])
        distance_z = object[0]
        distance_x = object[1]
        #calculates the distances of the edge points of the ball and the robot and the edge angles
        if(distance_z == 0):
            bounderies.append((180,0,object[2]))
        else:
            if(distance_x >= const.width()/2): #the object is right to the right corner of the robot
                distance_right = math.sqrt((distance_z)**2 + ((distance_x - const.ball_radius()) - const.width()/2)**2)
                distance_left = math.sqrt((distance_z-const.ball_radius())**2 + ((distance_x  + const.width()/2)**2))
                angle_left = math.asin(distance_z/distance_right)*180/math.pi
                angle_right = math.asin((distance_z-const.ball_radius())/distance_left)*180/math.pi

            elif(distance_x <= -(const.width()/2)): #the object is left to the left corner of the robot
                distance_right = math.sqrt((distance_z-const.ball_radius())**2 + ((distance_x  - const.width()/2)**2))
                distance_left = math.sqrt((distance_z)**2 + ((distance_x - const.ball_radius()) + const.width()/2)**2)
                angle_left = 180 - math.asin((distance_z-const.ball_radius())/distance_right)*180/math.pi
                angle_right = 180 - math.asin(distance_z/distance_left)*180/math.pi

            else: #the object is between the corners of the robot
                distance_right = math.sqrt((distance_z-const.ball_radius())**2 + ((distance_x  - const.width()/2)**2))
                distance_left = math.sqrt((distance_z-const.ball_radius())**2 + ((distance_x  + const.width()/2)**2))
                angle_left = 180 - math.asin((distance_z-const.ball_radius())/distance_right)*180/math.pi
                angle_right = math.asin((distance_z-const.ball_radius())/distance_left)*180/math.pi
            
            angle_left += const.safty_gap()*weight
            angle_right -= const.safty_gap()*weight
            if(angle_left > 180):
                angle_left = 180
            if(angle_right < 0):
                angle_right = 0
            bounderies.append((angle_left,angle_right,object[2]))
    return bounderies




    