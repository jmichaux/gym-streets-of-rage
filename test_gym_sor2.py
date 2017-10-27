import gym
import gym_sor

env = gym.make('StreetsOfRage2-Max-3-6-3-v0')
env.reset()
env.render()
#a = env.get_image()
#print(a)
while True:
	action=0
	env.step(action)
	env.render()
