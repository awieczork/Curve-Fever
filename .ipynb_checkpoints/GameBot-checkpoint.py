import numpy as np
import time
import cv2
import mss
import pyautogui as pyauto
import CurveFeverBot as cfb
from directKeys import PressKey, ReleaseKey, A, D

statusRefImg = cv2.imread('statusReferenceImage.png')

def PlayCurveFever(statusRefImg, color):
    # Settings

    colors = {
        'red' : np.array((69, 69, 255)),
        'pink' : np.array((186, 164, 255)),
        'yellow' : np.array((43, 233, 255)),
        'green': np.array((48, 255, 106)),
        'aqua': np.array((192, 209, 2)),
        'blue': np.array((255, 68, 68)),
        'orange': np.array((52, 136, 255))
    }
    full = {"top": 10, "left": 1320, "width": 2535 - 1320, "height": 1023 - 10}
    sct = mss.mss()
    PlayerColor = colors[color] # red
    colMin = PlayerColor - 20
    colMax = PlayerColor + 20
    states = []
    pyauto.click(x=1900, y=500)
    while 'Play':
        last_time = time.time()
        state1, status = cfb.GrabScreen(statusRefImg, sct, full, colMin, colMax)

        if status == 'Play':
            states.append(state1)
            if (len(states) == 3):
                p1, p2 = cfb.proccesTwoStates(states[0], states[1], states[2])
                fit, params, dists = cfb.getParameters(p1, p2)
                # imgView = cv2.line(state2,
                #                   (int(p2[0]), int(p2[1])),
                #                   (int(params['collisionPoint'][0]), int(params['collisionPoint'][1])),
                #                   (255, 255, 255),
                #                   2)

                # dodac odelglosc punkt przeciecia dla sladu
                print(cfb.checkPathCollsion(states[2], fit, params, p2))
                if cfb.checkPathCollsion(states[2], fit, params, p2):
                    PressKey(A)
                else:
                    ReleaseKey(A)

                if params['walldist'] > 150:
                    #print("UP   |", "DIST: ", params['walldist'], "ANGLE: ", params['angle']
                    ReleaseKey(A)
                else:
                    # print("DOWN |", "DIST: ", params['walldist'], "ANGLE: ", params['angle'])
                    # press = np.abs(params['angle']) * 1.2 / 180
                    PressKey(A)



                states.pop(0)

        # print("fps: {}".format(1 / (time.time() - last_time)))
                # print(status)
                # print(p1, p2)
                # print(fit)
                # print(params)
                # print(dists)
        #else:
            #imgView = state1
            #print(status)

        #cv2.imshow('View', imgView)

        #if cv2.waitKey(25) & 0xFF == ord("q"):
        #    cv2.destroyAllWindows()
        #    break


PlayCurveFever(statusRefImg, 'green')