from gym_curve.envs.curve_env import CurveEnv
import numpy as np
env = CurveEnv()

obs = env.reset()
for i in range(1500):

    env.render()
    # action = np.random.choice(env._possible_moves())
    action = "left"

    obs, rewards, done, info = env.step(action)

    #print(i, obs, action, info)
    #print(info)
    if done:
        print("DONE")
        obs = env.reset()

