import numpy as np
import time
import cv2
import mss
import pyautogui as pyauto
from scipy.spatial import distance

def firstNonEmpty(sums):
    a = 0
    i = 0
    while sums[i] == 0:
        a += 1
        i += 1
        if i == 898:
            break

    return a

def trimImage(imgArray, returnCoord=False):
    row = np.sum(imgArray, axis=1)
    col = np.sum(imgArray, axis=0)
    cEnd = firstNonEmpty(np.flip(col))
    cStart = firstNonEmpty(col)
    rEnd = firstNonEmpty(np.flip(row))
    rStart = firstNonEmpty(row)

    if cEnd == 0:
        cEnd = -col.size
    if rEnd == 0:
        rEnd = -row.size

    if returnCoord:
        return (np.array([[cStart, col.size - cEnd], [rStart, row.size - rEnd]]))

    return imgArray[rStart:-rEnd, cStart:-cEnd]

def makeDict(a, b, d):
    return (
        {'slope': a,
         'intercept': b,
         'direction': d}
    )

def getDirection(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if (x1 == x2 or y1 == y2):

        if (y1 == y2 and x1 > x2):
            return (makeDict(0, y1, -1))

        elif (y1 == y2 and x1 < x2):
            return (makeDict(0, y1, 1))

        elif (x1 == x2 and y2 > y1):
            return (makeDict(np.Inf, np.nan, -1))

        elif (x1 == x2 and y2 < y1):
            return (makeDict(np.Inf, np.nan, 1))

    else:
        a = (y1 - y2) / (x1 - x2)
        b = y1 - a * x1

        if (y2 > y1):
            d = -1
        else:
            d = 1

        return (makeDict(a, b, d))

def GrabScreen(statusRefImg):
    full = {"top": 10, "left": 1320, "width": 2535 - 1320, "height": 1023 - 10}
    board = {"top": 125, "left": 1637, "width": 898, "height": 898}
    pyauto.click(x=1900, y=500)
    ScreenFull1 = np.array(mss.mss().grab(full))[:, :, 0:3]
    time.sleep(0.01)
    ScreenState2 = np.array(mss.mss().grab(board))[:, :, 0:3]
    time.sleep(0.01)
    ScreenState3 = np.array(mss.mss().grab(board))[:, :, 0:3]

    if np.sum(ScreenFull1[0:25, 0:160, :] != statusRefImg) == 0:
        status = "Play"
    else:
        status = "Wait"

    ScreenState1 = ScreenFull1[115:, 317:, :]

    return ScreenState1, ScreenState2, ScreenState3, status


def proccesTwoStates(state1, state2, state3):
    # Filtering images
    state1Filter = cv2.inRange(state1, np.array((69, 69, 255)) - 20, np.array((69, 69, 255)) + 20)
    state2Filter = cv2.inRange(state2, np.array((69, 69, 255)) - 20, np.array((69, 69, 255)) + 20)
    state3Filter = cv2.inRange(state3, np.array((69, 69, 255)) - 20, np.array((69, 69, 255)) + 20)

    p1 = np.mean(np.flip(np.argwhere(state2Filter - state1Filter == 255)), axis=0)
    p2 = np.mean(np.flip(np.argwhere(state3Filter - state2Filter == 255)), axis=0)

    return p1, p2


def getCollisionPoint(fit, p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    a, b, d = fit.values()

    leftCond = np.array([
        b > 0 and b < 898 and a < 0 and d == -1,
        b > 0 and b < 898 and a > 0 and d == 1,
        b > 0 and b < 898 and a == 0 and d == -1
    ])

    yRight = 898 * a + b
    rightCond = np.array([
        yRight > 0 and yRight < 898 and a > 0 and d == -1,
        yRight > 0 and yRight < 898 and a < 0 and d == 1,
        a == 0 and d == 1
    ])

    topCond1 = np.array([
        d == 1 and a > 0 and b < 0,
        d == 1 and a < 0 and b > 0
    ])

    topCond2 = np.array([
        d == 1 and np.isinf(a)
    ])

    botCond1 = np.array([
        d == -1 and a > 0 and b < 898,
        d == -1 and a < 0 and b > 898
    ])

    botCond2 = np.array([
        d == -1 and np.isinf(a)
    ])

    if np.any(leftCond):
        xEnd = 0
        yEnd = b
        wall = 'left'
    elif np.any(rightCond):
        xEnd = 898
        yEnd = yRight
        wall = 'right'
    elif np.any(topCond1):
        xEnd = -b / a
        yEnd = 0
        wall = 'top'
    elif np.any(topCond2):
        xEnd = x2
        yEnd = 0
        wall = 'top'
    elif np.any(botCond1):
        xEnd = (898 - b) / a
        yEnd = 898
        wall = 'bot'
    elif np.any(botCond2):
        xEnd = x2
        yEnd = 898
        wall = 'bot'

    return xEnd, yEnd, wall


def getParameters(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    fit = getDirection(p1, p2)

    xEnd, yEnd, wall = getCollisionPoint(fit, p1, p2)

    distances = {
        'left': x2,
        'right': 898 - x2,
        'top': y2,
        'bottom': 898 - y2
    }

    params = {
        'collisionPoint': (xEnd, yEnd),
        'angle': np.arctan(fit['slope']) * 180 / np.pi,
        'wall': wall,
        'walldist': distance.cdist([(xEnd, yEnd)], [(x2, y2)], 'euclidean')[0][0]
    }

    return fit, params, distances