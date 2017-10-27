import itertools
import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

# SOR



# SOR2
game = 'StreetsOfRage2'
characters = ['Axel', 'Blaze', 'Max', 'Skate']
levels = [1, 2, 3, 4, 5, 6, 7, 8]
difficulty_options = [1, 2, 3, 4, 5, 6]
num_lives = [1, 2, 3, 4, 5, 6, 7, 8, 9]
probs = [0.0, 0.25] # repeat_action_probabilities

for env in itertools.product(characters, levels, difficulty_options, num_lives):
	character, level, difficulty, lives = env
	for obs_type in ['image', 'ram']:
		settings = '-'.join(str(e) for e in env)
		name = game + '-' + settings
		if obs_type == 'ram':
			name = '{}-ram'.format(name)
		nondeterministic = False
		
		for i, prob in enumerate(probs):
			register(
					id='{}-v'.format(name) + str(i),
					entry_point='gym_sor.envs:Sor2Env',
					kwargs={'obs_type': obs_type, 
									'repeat_action_probability': prob, 
									'character': character, 
									'difficulty': difficulty, 
									'num_lives': lives,
									'level': level},
					tags={'wrapper_config.TimeLimit.max_episode_steps': 10000},
					nondeterministic=nondeterministic,
		)
		



# SOR3
