import numpy as np

resolution = 320
write_to_files = False
color = 1 # red -> 0,   blue -> 1,   green -> 2,   yellow -> 3
text = "weight_exp_"

def matrix():
    if(resolution == 1024):
        return np.matrix([[494.1,    0. ,    526.4 ],
                 	      [   0.   ,491.5,   381.6 ],
                 	      [   0.,     0. ,     1.  ]])

    elif(resolution == 320):
        return np.matrix([[157.46059872,     0.       ,   166.09885972],
                          [  0.        , 156.49430644 ,   118.98524919],
                          [  0.        ,     0.       ,        1.     ]])
    elif(resolution == 416):
        return np.matrix([[202.47067627,     0.       ,   216.02996235],
                          [  0.        , 201.51621423 ,   156.82581336],
                          [  0.        ,     0.       ,        1.     ]])
    elif(resolution == 480):
        return np.matrix([[235.76823413,     0.       ,   252.18464158],
                          [  0.        , 234.79292837 ,   178.33909943],
                          [  0.        ,     0.       ,        1.     ]]) 
    elif(resolution == 512):
        return np.matrix([[251.75758536,     0.       ,   267.54448255],
                          [  0.        , 250.76510132 ,   189.8338372 ],
                          [  0.        ,     0.       ,        1.     ]])

    elif(resolution == 640):
        return np.matrix([[312.82853244,     0.       ,   328.93945098],
                          [  0.        , 311.19899836 ,   236.25011761],
                          [  0.        ,     0.       ,        1.     ]]) 

def dist():
    if(resolution == 1024):
        return np.matrix([[-3.32033416e-01 , 1.29692653e-01 ,-3.17310687e-05 ,-1.06236539e-04,-2.46108443e-02]])
    elif(resolution == 320):
        return np.matrix([[-0.37522101 , 0.26073798 , -0.00077529 , -0.00254424 , -0.13097464]])
    elif(resolution == 416):
        return np.matrix([[-0.35340774 ,  0.18862354  , -0.00225376 ,  -0.00043173 , -0.0671219 ]])
    elif(resolution == 480):
        return np.matrix([[-0.37096216 ,  0.24652116 , -0.00114937 , -0.00145204 , -0.11409468]])
    elif(resolution == 512):
        return np.matrix([[-3.74029430e-01 ,  2.50121215e-01 , -3.08985364e-04 , -3.66589029e-04 , -1.13610140e-01]])
    elif(resolution == 640):
        return np.matrix([[-3.59436754e-01 ,   2.11537467e-01 , -2.02586231e-04 , -8.90402899e-04 , -8.57309882e-02]])


def focal():
    mtx = matrix()
    return (mtx[0,0]+mtx[1,1])/2

def height():
    return 7.8851
    
def ball_radius():
    return 3

def width():
    return 9.9

def weight(dist):
    return 1/(1+1.2**(dist-22))

def weight_bound(dist):
    return 1/(1+1.6**(dist-20))

def safty_gap():
    return 50

def time_const_ui():
    return 0.7

def time_const_speed():
    return 0.2