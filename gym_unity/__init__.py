#import logging
from gym.envs.registration import registry, register, make, spec
#from gym.envs.gym_unity.unity_env import UnityEnv

#logger = logging.getLogger(__name__)

register(
    id='Unity-v0',
    entry_point='gym_unity.envs:UnityEnv',
    timestep_limit=1000,
    reward_threshold=1.0,
    nondeterministic = True,
)
