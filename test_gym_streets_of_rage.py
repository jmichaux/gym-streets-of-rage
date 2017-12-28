import gym
import gym_streets_of_rage


env = gym.make('streets_of_rage_ii_2_players-max-skate-3-4-v0')
env.reset()
env.render()
#a = env.get_image()
#print(a)
while True:
	env.step(16)
	env.render()
