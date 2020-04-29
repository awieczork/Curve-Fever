import numpy as np
import time
import cv2
import mss
import pyautogui as pyauto
import CurveFeverBotDEV as cfb

statusRefImg = cv2.imread('statusReferenceImage.png')

cv2.imshow("View", statusRefImg)
states = []
while 'Play':
    last_time = time.time()
    state1, status = cfb.GrabScreen(statusRefImg)



    if status == 'Play':
        states.append(state1)
        if (len(states) == 3):
            p1, p2 = cfb.proccesTwoStates(states[0], states[1], states[2])
            fit, params, dists = cfb.getParameters(p1, p2)
            #imgView = cv2.line(state2,
            #                   (int(p2[0]), int(p2[1])),
            #                   (int(params['collisionPoint'][0]), int(params['collisionPoint'][1])),
            #                   (255, 255, 255),
            #                   2)
            if params['walldist'] > 150:
                print("UP   |", "DIST: ", params['walldist'], "ANGLE: ", params['angle'])
                pyauto.keyUp('left')

            if params['walldist'] < 150:
                print("DOWN |", "DIST: ", params['walldist'], "ANGLE: ", params['angle'])
                pyauto.keyDown('left')


            states.pop(0)
            #print(status)
            #print(p1, p2)
            #print(fit)
            #print(params)
            #print(dists)
    else:
        imgView = state1
        print(status)

    cv2.imshow('View', imgView)

    print("fps: {}".format(1 / (time.time() - last_time)))
    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break