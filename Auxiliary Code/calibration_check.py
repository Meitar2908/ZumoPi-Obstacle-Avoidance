import cv2
import numpy as np
import os
import glob
import time

from numpy.core.fromnumeric import reshape


# Defining the dimensions of checkerboard
CHECKERBOARD = (6, 8)
# Creating vector to store vectors of 3D points for each checkerboard image
objpoints = []
# Creating vector to store vectors of 2D points for each checkerboard image
imgpoints = []


# Defining the world coordinates for 3D points
objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[0, :, :2] = np.mgrid[0:CHECKERBOARD[0],
                          0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None

# Extracting path of individual image stored in a given directory
images = glob.glob('./pictures/320/*.jpg')
i = 0
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    # If desired number of corners are found in the image then ret = true
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH +
                                             cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)

    """
    If desired number of corner are detected,
    we refine the pixel coordinates and display 
    them on the images of checker board
    """
    if ret == True:
        objpoints.append(objp)
        imgpoints.append(corners)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners, ret)

#     cv2.imshow('img', img)
#     cv2.waitKey(0)
#     i += 1

# cv2.destroyAllWindows()

h, w = img.shape[:2]

"""
Performing camera calibration by 
passing the value of known 3D points (objpoints)
and corresponding pixel coordinates of the 
detected corners (imgpoints)
"""
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None)

print("Camera matrix : \n")
print(mtx)
print("dist : \n")
print(dist)
# print("rvecs : \n")
# print(objpoints,imgpoints)
# print("tvecs : \n")
# print(tvecs)


images = glob.glob('./pictures/320/*.jpg')
i = 0
for file in images:
    img = cv2.imread(file)
    h,  w = img.shape[:2]
    # newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 0, (w, h))
    # undistort
    mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, mtx, (w, h), 5)
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
    # crop the image
    x, y, w, h = (25,25,295,215)
    dst = dst[y:h, x:w]
    print(dst.shape)
    cv2.imwrite("./pics/pics2/fixed/fixed"+str(i)+".jpg",dst)
    cv2.waitKey(0)
    i += 1
