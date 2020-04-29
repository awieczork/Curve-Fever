import numpy as np
import time
import cv2
import mss
import pyautogui as pyauto
import CurveFeverBotDEV as cfb

statusRefImg = cv2.imread('statusReferenceImage.png')

cv2.imshow("View", statusRefImg)
angle = []
while 'Play':
    last_time = time.time()
    state1, state2, state3, status = cfb.GrabScreen(statusRefImg)

    if status == 'Play':
        p1, p2 = cfb.proccesTwoStates(state1, state2, state3)
        fit, params, dists = cfb.getParameters(p1, p2)
        imgView = cv2.line(state2,
                           (int(p2[0]), int(p2[1])),
                           (int(params['collisionPoint'][0]), int(params['collisionPoint'][1])),
                           (255, 255, 255),
                           2)

        imgView = cv2.circle(imgView,
                            (int(p2[0]), int(p2[1])),
                            10,
                            (255, 255, 255),
                            2)

        angle.append(params['angle'])
        if len(angle) == 2:
            diff = np.abs(angle[1] - angle[0])

            print('DIST:', params['walldist'])
            if params['walldist'] >= 150 and diff > np.abs(angle[0]):
                # print("UP   |", "SLOPE: ", fit['slope'], "ANGLE: ", params['angle'])
                pyauto.keyUp('left')

            if params['walldist'] >= 150 and diff > np.abs(angle[0]):
                # print("UP   |", "SLOPE: ", fit['slope'], "ANGLE: ", params['angle'])
                pyauto.keyUp('right')

            angle.pop(0)


        #print("UP   |", "SLOPE: ", fit['slope'], "WALL: ", params['wall'], 'DIST: ', params['walldist'])
        if params['walldist'] < 150:
            key = 'None'
            if fit['slope'] >= 0:
                if params['wall'] in ['left', 'right']:
                    key = 'right'
                    pyauto.keyDown('right')
                elif params['wall'] in ['top', 'bot']:
                    key = 'left'
                    pyauto.keyDown('left')
            elif fit['slope'] < 0:
                if params['wall'] in ['left', 'right']:
                    key = 'left'
                    pyauto.keyDown('left')
                elif params['wall'] in ['top', 'bot']:
                    key = 'right'
                    pyauto.keyDown('right')

            print(key, "| SLOPE: ", fit['slope'], "WALL:", params['wall'], 'DIST:', params['walldist'])
            print('END')



        #print(status)
        #print(p1, p2)
        #print(fit)
        #print(params)
        #print(dists)
    else:
        imgView = state2
        print(status)

    cv2.imshow('View', imgView)

    #print("fps: {}".format(1 / (time.time() - last_time)))
    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break