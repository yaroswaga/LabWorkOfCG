import numpy as np
width = 1000
height = 1000
zoom = 5000
offset_x = width // 2 #смещение по х
offset_y = height // 2 #смещение по y
STEP_X = 0.1
STEP_Y = 0.1
STEP_Z = 0.1

start_t = (0.0, 0.0, 0.1)
persp_ref = 0.03
IMAGES = "images"
OBJECTS = "objects"
light = np.array([0, 0, 1])