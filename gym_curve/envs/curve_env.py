import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

# Actions:
# RIGHT   =  1
# LEFT    = -1
# FORWARD =  0


class CurveEnv(gym.Env):
    metadata = {'render.modes' : ['human', 'rgb_array']}


    def __init__(self):
        self.state = np.zeros((3))

        self.state[0] = np.random.randint(0 + 200, 898 - 200, 1)
        self.state[1] = np.random.randint(0 + 200, 898 - 200, 1)
        self.state[2] = np.random.choice(np.round(np.linspace(0, 360, 120)))

        self.frame = 0 # Counter
        self.done = False # End episode Flag
        self.add = [] # Info
        self.reward = 0 #
        self.radius = 5 # Player radius
        self.speed = 1.8572830964234517 # Distance per frame
        self.board = np.zeros((898, 898)) # Main game screen
        self.boardHIST = np.zeros((898, 898)) # Second screen - 5 frames ahead

    def step(self, move):

        if self.done == True:
            print("Game Over")
            return [self.state, self.reward, self.done, self.add]
        elif move == -1:

            if move == 'left':
                angle -= 3.25
            elif move == 'right':
                angle += 3.25
        if


