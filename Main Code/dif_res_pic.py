import time
import picamera

def picture_with_set_res(i,res = (1024,768)):
    camera = picamera.PiCamera()
    try:
        camera.resolution = res
        camera.start_preview()
        time.sleep(2)
        camera.capture('/home/pi/WS_Zumo/ZumoObstacles/pictures/'+str(res[0]) + 'X' + str(res[1]) +'#'+ str(i) + '.jpg')
        camera.stop_preview()
    finally:
        camera.close()



res_list = []
inp = input("Enter res:")
inp1 = int(inp)/4*3
while("N" != inp):
    print()
    res_list.append((int(inp),int(inp1)))
    inp = input("Enter another res or N to stop: ")
    if(inp.isnumeric()):
        inp1 = int(inp)/4*3   
i = 2
inp = "Y"
while("N" != inp):
    for res in res_list:
        picture_with_set_res(i,res)
    inp = input("Y to continue, N to stop: ")
    i += 1

