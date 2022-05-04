
# # import required modules
#!/usr/bin/python3
from pydoc import classname
import threading
import serial
import time
import math
import cv2
import control
import camera_stream as cam
import constants as const

#dash imports
import dash
from dash import dcc
import dash_daq as daq
from dash import html
import logging
from flask import Flask, Response


# serial connection
ser = serial.Serial('/dev/ttyACM0')  # open serial port

# variables
global zumoAngle, zumoSpeed, camera_stream, frame, clicks, speed
global battery, joy_speed, joy_angle, fixed_frame, fps, frame_kind
clicks_mutex = threading.Lock()

server = Flask(__name__)
app = dash.Dash(__name__, server = server)



app.layout = html.Div([
    dcc.Interval(
    id="load_interval", 
    n_intervals=0,
    interval = const.time_const_ui()*1000 
    ),
    daq.Joystick(
        id='my-joystick',
        label="Zumo Joystick",
        angle=0,
        force=0,
        size = 700,
        style = {'position': 'fixed','dispaly': 'block', 'top': '10%','left': '10%','background-color': '#181818'}
    ),
    html.Div(id='joystick-output'),html.Div(id='data-output'),
    html.Div(html.Button(
      'Activate Obstacles Avoidance',
      id='Auto Drive',
      value='navigation',
      style = {'position': 'fixed','top': '70%','left': '10%','height': '5%','width': '25%'},
      n_clicks=0,)),
    html.Div([
      html.Img(
        src="/camera_stream",
        style = {'position': 'fixed','top': '10%','left': '50%','height': '60%','width': '45%'}),
      daq.Thermometer(
        id='thermometer',
        label = "Speed Value",
        value=0,
        min=-20,
        max=20,
        style = {'position': 'fixed','top': '75%','left': '65%'}),
        daq.Gauge(
        id='gauge',
        label="Speed Angle",
        value=90,
        max = 225,
        min = -45,
        style = {'position': 'fixed','top': '75%','left': '70%'}),
      ]),
    html.Div(html.Button(
      'Show Object Detection',
      id='Frame Kind',
      value='navigation',
      style = {'position': 'fixed','top': '80%','left': '10%','height': '5%','width': '20%'},
      n_clicks=0,))
],)


@server.route('/camera_stream')
def video_feed():
    return Response(Camera_handler(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.callback(
    dash.dependencies.Output(component_id="data-output", component_property="children"),
    dash.dependencies.Input(component_id="load_interval", component_property="n_intervals"),
)
def update_fps(n_intervals:int):
    global battery,fps
    return ['Battery charging: {}'.format(battery),
            html.Br(),
            'fps: {}'.format(round(fps,2)),]

@app.callback(
    dash.dependencies.Output(component_id="thermometer", component_property="value"),
    dash.dependencies.Input(component_id="load_interval", component_property="n_intervals"),
)
def update_speed(n_intervals:int):
    global speed
    return round(speed[0],2)

@app.callback(
    dash.dependencies.Output(component_id="gauge", component_property="value"),
    dash.dependencies.Input(component_id="load_interval", component_property="n_intervals"),)
def update_speed(n_intervals:int):
    global speed
    return 180 - int(speed[1])

@app.callback(
    dash.dependencies.Output('joystick-output', 'children'),
    [dash.dependencies.Input('my-joystick', 'angle'),
     dash.dependencies.Input('my-joystick', 'force'),
     dash.dependencies.Input(component_id="load_interval", component_property="n_intervals")])
def update_output(angle, force,n_intervals):
    global joy_angle, joy_speed
    if type(force) == int or float:
      joy_speed = force
    else:
      joy_speed = 0
    if (type(angle) == int or float) and joy_speed != 0:
      joy_angle = angle
    else:
      joy_angle = 0
    return ['Angle is {}'.format(angle),
            html.Br(),
            'Force is {}'.format(force),]


@app.callback(dash.dependencies.Output('Auto Drive', 'style'),
             [dash.dependencies.Input('Auto Drive', 'n_clicks')])
def change_button_style(n_clicks):
    global clicks
    clicks = n_clicks
    if n_clicks % 2 == 0:
        return {'position': 'fixed','top': '70%','left': '10%','height': '5%','width': '700px'}
    else:
        return {'position': 'fixed','top': '70%','left': '10%','height': '5%','width': '700px', 'background-color': '#4efc03'}


@app.callback(dash.dependencies.Output('Frame Kind', 'style'),
             [dash.dependencies.Input('Frame Kind', 'n_clicks')])
def change_button_style(n_clicks):
    global frame_kind
    frame_kind = n_clicks % 2
    if frame_kind:
        return {'position': 'fixed','top': '80%','left': '10%','height': '5%','width': '700px', 'background-color': '#4efc03'}
    else:
        return {'position': 'fixed','top': '80%','left': '10%','height': '5%','width': '700px'}

def start_app():
    app.server.run(port=8100, host='0.0.0.0')

def TransmitThread():
  #intializes the the frame counter and captures start time for calculating fps
  frames_counter = 1
  start_time = time.time()
  reset_time = 1
  while ser.isOpen:
    global zumoSpeed, zumoAngle, clicks, joy_angle, joy_speed
    global frame, fixed_frame, fps, frame_kind, speed
    clicks_mutex.acquire()
    is_manual = (clicks % 2 == 0)
    clicks_mutex.release()
    #reset the fps calculation when switching modes
    if(not is_manual and reset_time):
      start_time = time.time()
      frames_counter = 1
      reset_time = 0
    elif(is_manual and not reset_time):
      start_time = time.time()
      frames_counter = 1
      reset_time = 1
    #gets the corrected speed and angle
    zumoSpeed, zumoAngle, fixed_frame, speed = control.auto_drive(frame,joy_speed,joy_angle,is_manual,frame_kind)
    #calculates the fps
    current_time = time.time()
    fps = 1/((current_time - start_time)/frames_counter)
    frames_counter += 1
    #sends speed and angle to the robot
    joyY = math.sin(math.radians(zumoAngle))*zumoSpeed*200/(1.2-is_manual*0.2)
    joyX = math.cos(math.radians(zumoAngle))*zumoSpeed*200/(1.2-is_manual*0.2)
    if(battery):
      joyY = math.sin(math.radians(zumoAngle))*zumoSpeed*200*2
    msg = ''
    msg = str(joyX) + ',' +str(joyY) +'\r\n'
    ser.write(msg.encode('ascii'))
    time.sleep(0.02)

def ReceiveThread():
  while ser.isOpen:
    global battery
    if ser.in_waiting > 0:
      line = ser.readline().decode("ascii")
      if(len(line.split()) == 5 and line.split()[4] != ","):
        battery = float(line.split()[4]) > 4
      else:
        print(line)
    else:
      time.sleep(0.05)

def Camera_handler():
  while(ser.isOpen):
    global frame, camera_stream, fixed_frame, frame_kind
    frame = camera_stream.read()
    if(frame_kind):
      ret,jpg = cv2.imencode('.jpg', fixed_frame)
    else:
      ret,jpg = cv2.imencode('.jpg', frame)
    jpg_byets = jpg.tobytes()
    yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + jpg_byets + b'\r\n\r\n')

def initializeThreads():
  global zumoAngle, zumoSpeed, camera_stream,clicks,battery
  global joy_angle, joy_speed, frame, fps, frame_kind,speed
  #initialize global parameters
  zumoAngle = 0 
  zumoSpeed = 0
  joy_speed = 0
  joy_angle = 0
  clicks = 0
  battery = 0
  frame = None
  fps = 0
  frame_kind = 0
  speed = (0,0)
  camera_stream = cam.PiVideoStream((const.resolution,int(const.resolution/4*3)))
  camera_stream.start()
  time.sleep(2)
  # supress logging
  log = logging.getLogger('werkzeug')
  log.setLevel(logging.ERROR)
  
  #define threads, and start them
  t1 = threading.Thread(target=TransmitThread)
  t2 = threading.Thread(target=ReceiveThread)
  t3 = threading.Thread(target=start_app) 
  t1.start()
  t2.start()
  t3.start()

if __name__ == "__main__":
  initializeThreads()
    
    
    