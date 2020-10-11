import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import cv2
from scipy.spatial import distance
# Actions:
# RIGHT   =  1
# LEFT    = -1
# FORWARD =  0


def draw(img, X, Y):
    cv2.circle(img, (X, Y), int(4), (255, 255, 255), -1)

class CurveEnv(gym.Env):
    metadata = {'render.modes' : ['human', 'rgb_array']}

    def __init__(self):
        self.memory = None
        self.state = None
        self.frame = 0 # Counter
        self.done = False # End episode Flag
        self.add = [] # Info
        self.reward = 0 #
        self.radius = 5 # Player radius
        self.speed = 1.8 #1.8572830964234517 # Distance per frame
        self.tickangel = 3# 3.25
    def _possible_moves(self):
        return np.array(['left', 'right', 'forward'])

    def reset(self):
        self.done = False
        # Main game screen
        self.board = np.zeros((898, 898))
        self.boardHIST = np.zeros((898, 898))

        # Starting coordinates - RANDOM
        # self.x = np.random.randint(0 + 200, 898 - 200, 1)
        # self.y = np.random.randint(0 + 200, 898 - 200, 1)
        # self.angle = np.random.choice(np.round(np.linspace(0, 360, 120)))

        # Starting coordinates - FIXED
        self.x = np.array([449])
        self.y = np.array([449])
        self.angle = 359 # 360 - 45 # 0.0
        self.intercept = self.y[-1] - self.x[-1] * np.tan(self.angle * np.pi)
        self.slope = 0
        # State
        self.state = [self.x, self.y, self.angle]
        self.memory = [[self.x[-1], self.y[-1], self.angle, self.intercept, "start"]]
        # Drawing position
        draw(self.board, self.x, self.y)
        draw(self.boardHIST, self.x, self.y)

        return np.array(self.state)

    def step(self, move):
        self.frame += 1


        # If done
        if self.done == True:
            print("Game Over", self.frame)
            return self.state, self.reward, self.done, self.add

        if move == 'left':
            self.angle -= self.tickangel
        elif move == 'right':
            self.angle += self.tickangel

        if self.angle >= 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360

        newX = self.x[-1] + int(1.7 * self.speed * np.cos(self.angle * np.pi / 180))
        newY = self.y[-1] + int(1.7 * self.speed * np.sin(self.angle * np.pi / 180))
        self.x = np.append(self.x, newX)
        self.y = np.append(self.y, newY)

        points = np.asarray(np.nonzero(self.board))
        y = -points[0][:]
        x = points[1][:]
        self.slope = np.tan((360 - self.angle) * np.pi/180)
        self.intercept = -self.y[-1] - self.x[-1] * self.slope


        dist = np.abs(-self.slope * x + y - self.intercept) / np.sqrt((-self.slope) ** 2 + 1 ** 2)

        a = (360 - self.angle)
        if (0 <= a < 90 or 270 < a):
            dist = np.abs(-self.slope * x + y - self.intercept) / np.sqrt((-self.slope) ** 2 + 1 ** 2)
            xR = x[(dist < 1) & (x > self.x[-1])]
            yR = y[(dist < 1) & (x > self.x[-1])]
            xDiff = xR - self.x[-1]
            distX = xR[xDiff > 2] - self.x[-1]
            distY = yR[xDiff > 2] + self.y[-1]
            distR = np.sqrt(distX**2 + distY**2)
            if distR.shape[0] > 0:
                print(np.min(distR))
            elif 0 <= a < 45 or 315 < a:
                dst = distance.euclidean((self.x[-1], -self.y[-1]), (898, self.slope * 898 + self.intercept))
                print(dst)
            elif 45 <= a < 90:
                dst = distance.euclidean((self.x[-1], -self.y[-1]), (self.intercept/(-self.slope), 0))
                print(dst)
            elif 270 <= a < 315:
                dst = distance.euclidean((self.x[-1], -self.y[-1]), (self.intercept / (-self.slope), -898))
                print(dst)

        elif 90 < a < 270:
            dist = np.abs(-self.slope * x + y - self.intercept) / np.sqrt((-self.slope) ** 2 + 1 ** 2)
            xR = x[(dist < 1) & (x < self.x[-1])]
            yR = y[(dist < 1) & (x < self.x[-1])]
            xDiff = xR - self.x[-1]
            distX = xR[xDiff > 2] - self.x[-1]
            distY = yR[xDiff > 2] + self.y[-1]
            distR = np.sqrt(distX ** 2 + distY ** 2)
            if distR.shape[0] > 0:
                print(np.min(distR))
            elif 90 <= a < 135:
                dst = distance.euclidean((self.x[-1], -self.y[-1]), (self.intercept/(-self.slope), 0))
                print(dst)
            elif 135 <= a < 225:
                dst = distance.euclidean((self.x[-1], -self.y[-1]), (0, self.slope * 898 + self.intercept))
                print(dst)
            elif 225 <= a < 270:
                dst = distance.euclidean((self.x[-1], -self.y[-1]), (self.intercept / (-self.slope), -898))
                print(dst)

        self.state = [self.x, self.y, self.angle]

        check1 = bool(
            self.x[-1] >= 898
            or self.x[-1] < 0
            or self.y[-1] >= 898
            or self.y[-1] < 0
        )

        if not check1 and self.x.shape[0] == 4:
            check2 = bool(self.boardHIST[self.y[-1], self.x[-1]] != 0) #
            draw(self.boardHIST, self.x[1], self.y[1])
            self.x = np.delete(self.x, 0)
            self.y = np.delete(self.y, 0)
        else:
            check2 = False

        draw(self.board, self.x[-1], self.y[-1])


        self.done = bool(
            check1 or check2
        )

        self.memory = np.concatenate((self.memory, [[self.x[-1], self.y[-1], self.angle, self.intercept, move]]))
        self.add = [self.memory, points]
        if self.done:
            self.reward = 0
            return self.state, self.reward, self.done, self.add
        else:
            self.reward = 1
            return self.state, self.reward, self.done, self.add



    def render(self):

        cv2.imshow('Curve', self.board)

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()

