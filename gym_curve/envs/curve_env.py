import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import cv2

# Actions:
# RIGHT   =  1
# LEFT    = -1
# FORWARD =  0


def draw(img, X, Y):
    cv2.circle(img, (X, Y), int(4), (255, 255, 255), -1)

class CurveEnv(gym.Env):
    metadata = {'render.modes' : ['human', 'rgb_array']}

    def __init__(self):

        self.state = None
        self.frame = 0 # Counter
        self.done = False # End episode Flag
        self.add = [] # Info
        self.reward = 0 #
        self.radius = 5 # Player radius
        self.speed = 1.8572830964234517 # Distance per frame

    def _possible_moves(self):
        return np.array(['left', 'right', 'forward'])

    def reset(self):

        # Main game screen
        self.board = np.zeros((898, 898))
        self.boardHIST = np.zeros((898, 898))

        # Starting coordinates
        self.x = np.random.randint(0 + 200, 898 - 200, 1)
        self.y = np.random.randint(0 + 200, 898 - 200, 1)
        self.angle = np.random.choice(np.round(np.linspace(0, 360, 120)))

        # State
        self.state = [self.x, self.y, self.angle]

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
            self.angle -= 3.25
        elif move == 'right':
            self.angle += 3.25

        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 360:
            self.angle += 360

        self.x = np.append(self.x, self.x[-1] + int(1.7 * self.speed * np.cos(self.angle * np.pi / 180)))
        self.y = np.append(self.y, self.y[-1] + int(1.7 * self.speed * np.sin(self.angle * np.pi / 180)))

        self.state = [self.x, self.y, self.angle]

        check1 = bool(
            self.x[-1] >= 898
            or self.x[-1] < 0
            or self.y[-1] >= 898
            or self.y[-1] < 0
        )

        if not check1 and self.x.shape[0] == 4:
            check2 = bool(self.boardHIST[self.y[-1], self.x[-1]] != 0)
            draw(self.boardHIST, self.x[1], self.y[1])
            self.x = np.delete(self.x, 0)
            self.y = np.delete(self.y, 0)
        else:
            check2 = False

        draw(self.board, self.x[-1], self.y[-1])


        self.done = bool(
            check1 or check2
        )


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

