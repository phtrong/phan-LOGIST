import keyboard
import mss
import cv2
import numpy
from time import time, sleep
import pyautogui

pyautogui.PAUSE = 0

print("Press 's' to start playing.")
print("Once started press 'q' to quit.")
keyboard.wait('s')
left = True
x = 1250
y = 700
sct = mss.mss()
dimensions_left = {
        'left': 1100,
        'top': 400,
        'width': 300,
        'height': 150
    }

dimensions_right = {
        'left': 1500,
        'top': 400,
        'width': 300,
        'height': 150
    }

wood_left = cv2.imread('woodleft1.png')

wood_right = cv2.imread('woodright1.png')
w = wood_left.shape[1]
h = wood_left.shape[0]

fps_time = time()
while True:

    if left:
        scr = numpy.array(sct.grab(dimensions_left))
        wood = wood_left
    else:
        scr = numpy.array(sct.grab(dimensions_right))
        wood = wood_right

    # Cut off alpha
    scr_remove = scr[:,:,:3]

    result = cv2.matchTemplate(scr_remove, wood, cv2.TM_CCOEFF_NORMED)
    
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    print(f"Max Val: {max_val} Max Loc: {max_loc}")
    src = scr.copy()
    if max_val > .85:
        left = not left
        if left:
            x=1100
        else:
            x=1600
        cv2.rectangle(scr, max_loc, (max_loc[0] + w, max_loc[1] + h), (0,255,255), 2)

    cv2.imshow('Screen Shot', scr)
    cv2.waitKey(1)
    pyautogui.click(x=x, y=y)
    sleep(.1)
    if keyboard.is_pressed('q'):
        break

    print('FPS: {}'.format(1 / (time() - fps_time)))
    fps_time = time()