from gym_curve.envs.curve_env import CurveEnv
import numpy as np
env = CurveEnv()

obs = env.reset()
print(obs)
for i in range(2000):
    action = np.random.choice(env._possible_moves())
    obs, rewards, done, info = env.step(action)
    env.render()
    if done:
        print(env.frame)
        break