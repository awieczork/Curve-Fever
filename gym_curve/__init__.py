from gym.envs.registration import register

register(
    id='curve-v0',
    entry_point='gym_curve.envs:CurveEnv',
)