import sys
# sys.path.append('.')
import gym
import gym_super_mario_bros as gsmb

env = gym.make('SuperMarioBros-v2')

done = True
for step in range(5000):
    if done:
        state = env.reset()
    state, reward, done, info = env.step(env.action_space.sample())

env.close()
