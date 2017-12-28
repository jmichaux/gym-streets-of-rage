import itertools
import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)



##########################  

#     SOR ONE PLAYER     #

##########################

game = 'streets_of_rage'
player_a_characters = ['adam', 'axel', 'blaze']
start_levels = [1, 2, 3, 4, 5, 6, 7]
end_levels = [1, 2, 3, 4, 5, 6, 7]
difficulty_settings = [1, 2, 3, 4, 5, 6]
num_lives = [1, 3, 5, 7, 9]
probs = [0.0, 0.25] # repeat_action_probabilities

for env in itertools.product(player_a_characters, start_levels, difficulty_settings):
    player_a, start_level, difficulty = env
    for obs_type in ['image', 'ram']:
          settings = '-'.join(str(e) for e in env)
          name = game + '-' + settings
          if obs_type == 'ram':
              name = '{}-ram'.format(name)
          nondeterministic = False
          for i, prob in enumerate(probs):
              
              # Nondeterministic frame skip.
              register(
                  id='{}-v'.format(name) + str(i),
                  entry_point='gym_streets_of_rage.envs:SorEnv',
                  kwargs={'game': game, 'obs_type': obs_type, 
                          'repeat_action_probability': prob, 
                          'player_a': player_a,  
                          'start_level': start_level,  
                          'difficulty': difficulty,},
                  max_episode_steps=100000,
                  nondeterministic=nondeterministic,
              )

              # Deterministic frame skip = 4.
              register(
                  id='{}-Deterministic-v'.format(name)+ str(i),
                  entry_point='gym_streets_of_rage.envs:SorEnv',
                  kwargs={'game': game, 'obs_type': obs_type, 'frameskip': 4, 
                          'repeat_action_probability': prob, 
                          'player_a': player_a,  
                         'start_level': start_level,
                          'difficulty': difficulty,},
                  max_episode_steps=100000,
                  nondeterministic=nondeterministic,
              )

              # No frameskip. This means keep every frame.
              register(
                  id='{}-NoFrameskip-v4'.format(name)+ str(i),
                  entry_point='gym_streets_of_rage.envs:SorEnv',
                  kwargs={'game': game, 'obs_type': obs_type, 'frameskip': 1, 
                          'repeat_action_probability': prob,
                          'player_a': player_a,  
                         'start_level': start_level,
                          'difficulty': difficulty,},
                  max_episode_steps=100000,
                  nondeterministic=nondeterministic,
              )


###########################  

#     SOR TWO PLAYERS     #

###########################

game = 'streets_of_rage_2_players'
player_a_characters = ['Adam', 'axel', 'blaze']
player_b_characters = ['Adam', 'axel', 'blaze']
start_levels = [1, 2, 3, 4, 5, 6, 7, 8]
end_levels = [1, 2, 3, 4, 5, 6, 7, 8]
difficulty_settings = [1, 2, 3, 4, 5, 6]
num_lives = [1, 3, 5, 7, 9]
probs = [0.0, 0.25] # repeat_action_probabilities

for env in itertools.product(player_a_characters, player_b_characters, start_levels, difficulty_settings):
    player_a, player_b, start_level, difficulty = env
    for obs_type in ['image', 'ram']:
        if (player_a != player_b):
            settings = '-'.join(str(e) for e in env)
            name = game + '-' + settings
            if obs_type == 'ram':
                name = '{}-ram'.format(name)
            nondeterministic = False
            for i, prob in enumerate(probs):
                
                # Nondeterministic frame skip.
                register(
                    id='{}-v'.format(name) + str(i),
                    entry_point='gym_streets_of_rage.envs:SorEnv',
                    kwargs={'game': game, 'obs_type': obs_type, 
                            'repeat_action_probability': prob, 
                            'player_a': player_a, 'player_b': player_b, 
                            'start_level': start_level, 
                            'difficulty': difficulty,},
                    max_episode_steps=100000,
                    nondeterministic=nondeterministic,
                )

                # Deterministic frame skip = 4.
                register(
                    id='{}-Deterministic-v'.format(name)+ str(i),
                    entry_point='gym_streets_of_rage.envs:SorEnv',
                    kwargs={'game': game, 'obs_type': obs_type, 'frameskip': 4, 
                            'repeat_action_probability': prob, 
                            'player_a': player_a, 'player_b': player_b, 
                            'start_level': start_level,  
                            'difficulty': difficulty,},
                    max_episode_steps=100000,
                    nondeterministic=nondeterministic,
                )

                # No frameskip. This means keep every frame.
                register(
                    id='{}-NoFrameskip-v4'.format(name)+ str(i),
                    entry_point='gym_streets_of_rage.envs:SorEnv',
                    kwargs={'game': game, 'obs_type': obs_type, 'frameskip': 1, 
                            'repeat_action_probability': prob,
                            'player_a': player_a, 'player_b': player_b, 
                            'start_level': start_level,  
                            'difficulty': difficulty,},
                    max_episode_steps=100000,
                    nondeterministic=nondeterministic,
                )




##########################  

#    SOR2 ONE PLAYER     #

##########################
game = 'streets_of_rage_ii'
player_a_characters = ['axel', 'blaze', 'max', 'skate']
start_levels = [1, 2, 3, 4, 5, 6, 7, 8]
difficulty_settings = [1, 2, 3, 4, 5, 6]
num_lives = [3]
probs = [0.0, 0.25] # repeat_action_probabilities

for env in itertools.product(player_a_characters, start_levels, difficulty_settings):
    player_a, start_level, difficulty = env
    for obs_type in ['image', 'ram']:
          settings = '-'.join(str(e) for e in env)
          name = game + '-' + settings
          if obs_type == 'ram':
              name = '{}-ram'.format(name)
          nondeterministic = False
          for i, prob in enumerate(probs):
              
              # Nondeterministic frame skip.
              register(
                  id='{}-v'.format(name) + str(i),
                  entry_point='gym_streets_of_rage.envs:SorEnv',
                  kwargs={'game': game, 'obs_type': obs_type, 
                          'repeat_action_probability': prob, 
                          'player_a': player_a,  
                          'start_level': start_level,  
                          'difficulty': difficulty,},
                  max_episode_steps=100000,
                  nondeterministic=nondeterministic,
              )

              # Deterministic frame skip = 4.
              register(
                  id='{}-Deterministic-v'.format(name)+ str(i),
                  entry_point='gym_streets_of_rage.envs:SorEnv',
                  kwargs={'game': game, 'obs_type': obs_type, 'frameskip': 4, 
                          'repeat_action_probability': prob, 
                          'player_a': player_a,  
                         'start_level': start_level,
                          'difficulty': difficulty,},
                  max_episode_steps=100000,
                  nondeterministic=nondeterministic,
              )

              # No frameskip. This means keep every frame.
              register(
                  id='{}-NoFrameskip-v4'.format(name)+ str(i),
                  entry_point='gym_streets_of_rage.envs:SorEnv',
                  kwargs={'game': game, 'obs_type': obs_type, 'frameskip': 1, 
                          'repeat_action_probability': prob,
                          'player_a': player_a,  
                         'start_level': start_level,
                          'difficulty': difficulty,},
                  max_episode_steps=100000,
                  nondeterministic=nondeterministic,
              )



###########################  

#     SOR2 TWO PLAYERS    #

###########################
                    
game = 'streets_of_rage_ii_2_players'
player_a_characters = ['axel', 'blaze', 'max', 'skate']
player_b_characters = ['axel', 'blaze', 'max', 'skate']
start_levels = [1, 2, 3, 4, 5, 6, 7, 8]
end_levels = [1, 2, 3, 4, 5, 6, 7, 8]
difficulty_settings = [1, 2, 3, 4, 5, 6]
num_lives = [1, 2, 3, 4, 5, 6, 7, 8, 9]
probs = [0.0, 0.25] # repeat_action_probabilities

for env in itertools.product(player_a_characters, player_b_characters, start_levels, difficulty_settings):
    player_a, player_b, start_level, difficulty = env
    for obs_type in ['image', 'ram']:
        if (player_a != player_b):
            settings = '-'.join(str(e) for e in env)
            name = game + '-' + settings
            if obs_type == 'ram':
                name = '{}-ram'.format(name)
            nondeterministic = False
            for i, prob in enumerate(probs):
                
                # Nondeterministic frame skip.
                register(
                    id='{}-v'.format(name) + str(i),
                    entry_point='gym_streets_of_rage.envs:SorEnv',
                    kwargs={'game': game, 'obs_type': obs_type, 
                            'repeat_action_probability': prob, 
                            'player_a': player_a, 'player_b': player_b, 
                            'start_level': start_level,  
                            'difficulty': difficulty,},
                    max_episode_steps=100000,
                    nondeterministic=nondeterministic,
                )

                # Deterministic frame skip = 4.
                register(
                    id='{}-Deterministic-v'.format(name)+ str(i),
                    entry_point='gym_streets_of_rage.envs:SorEnv',
                    kwargs={'game': game, 'obs_type': obs_type, 'frameskip': 4, 
                            'repeat_action_probability': prob, 
                            'player_a': player_a, 'player_b': player_b, 
                            'start_level': start_level,  
                            'difficulty': difficulty,},
                    max_episode_steps=100000,
                    nondeterministic=nondeterministic,
                )

                # No frameskip. This means keep every frame.
                register(
                    id='{}-NoFrameskip-v4'.format(name)+ str(i),
                    entry_point='gym_streets_of_rage.envs:SorEnv',
                    kwargs={'game': game, 'obs_type': obs_type, 'frameskip': 1, 
                            'repeat_action_probability': prob,
                            'player_a': player_a, 'player_b': player_b, 
                            'start_level': start_level,  
                            'difficulty': difficulty,},
                    max_episode_steps=100000,
                    nondeterministic=nondeterministic,
                )



###########################  

#     SOR3 ONE PLAYER     #

###########################
                    
game = 'streets_of_rage_iii'
player_a_characters = ['axel', 'blaze', 'skate', 'zan']
start_levels = [1, 2, 3, 4, 5, 6, 7, 8]
end_levels = [1, 2, 3, 4, 5, 6, 7, 8]
difficulty_settings = [1, 2, 3, 4, 5, 6]
num_lives = [1, 2, 3, 4, 5, 6, 7, 8, 9]
probs = [0.0, 0.25] # repeat_action_probabilities

for env in itertools.product(player_a_characters, start_levels, difficulty_settings):
    player_a, start_level, difficulty = env
    for obs_type in ['image', 'ram']:
          settings = '-'.join(str(e) for e in env)
          name = game + '-' + settings
          if obs_type == 'ram':
              name = '{}-ram'.format(name)
          nondeterministic = False
          for i, prob in enumerate(probs):
              
              # Nondeterministic frame skip.
              register(
                  id='{}-v'.format(name) + str(i),
                  entry_point='gym_streets_of_rage.envs:SorEnv',
                  kwargs={'game': game, 'obs_type': obs_type, 
                          'repeat_action_probability': prob, 
                          'player_a': player_a,  
                          'start_level': start_level,  
                          'difficulty': difficulty,},
                  max_episode_steps=100000,
                  nondeterministic=nondeterministic,
              )

              # Deterministic frame skip = 4.
              register(
                  id='{}-Deterministic-v'.format(name)+ str(i),
                  entry_point='gym_streets_of_rage.envs:SorEnv',
                  kwargs={'game': game, 'obs_type': obs_type, 'frameskip': 4, 
                          'repeat_action_probability': prob, 
                          'player_a': player_a,  
                         'start_level': start_level,
                          'difficulty': difficulty,},
                  max_episode_steps=100000,
                  nondeterministic=nondeterministic,
              )

              # No frameskip. This means keep every frame.
              register(
                  id='{}-NoFrameskip-v4'.format(name)+ str(i),
                  entry_point='gym_streets_of_rage.envs:SorEnv',
                  kwargs={'game': game, 'obs_type': obs_type, 'frameskip': 1, 
                          'repeat_action_probability': prob,
                          'player_a': player_a,  
                         'start_level': start_level,
                          'difficulty': difficulty,},
                  max_episode_steps=100000,
                  nondeterministic=nondeterministic,
              )


###########################  

#     SOR3 TWO PLAYERS    #

###########################
                    
game = 'streets_of_rage_iii_2_players'
player_a_characters = ['axel', 'blaze', 'skate', 'zan']
player_b_characters = ['axel', 'blaze', 'skate', 'zan']
start_levels = [1, 2, 3, 4, 5, 6, 7, 8]
end_levels = [1, 2, 3, 4, 5, 6, 7, 8]
difficulty_settings = [1, 2, 3, 4, 5, 6]
num_lives = [1, 2, 3, 4, 5, 6, 7, 8, 9]
probs = [0.0, 0.25] # repeat_action_probabilities

for env in itertools.product(player_a_characters, player_b_characters, start_levels, difficulty_settings):
    player_a, player_b, start_level, difficulty = env
    for obs_type in ['image', 'ram']:
        if (player_a != player_b):
            settings = '-'.join(str(e) for e in env)
            name = game + '-' + settings
            if obs_type == 'ram':
                name = '{}-ram'.format(name)
            nondeterministic = False
            for i, prob in enumerate(probs):
                
                # Nondeterministic frame skip.
                register(
                    id='{}-v'.format(name) + str(i),
                    entry_point='gym_streets_of_rage.envs:SorEnv',
                    kwargs={'game': game, 'obs_type': obs_type, 
                            'repeat_action_probability': prob, 
                            'player_a': player_a, 'player_b': player_b, 
                            'start_level': start_level,  
                            'difficulty': difficulty,},
                    max_episode_steps=100000,
                    nondeterministic=nondeterministic,
                )

                # Deterministic frame skip = 4.
                register(
                    id='{}-Deterministic-v'.format(name)+ str(i),
                    entry_point='gym_streets_of_rage.envs:SorEnv',
                    kwargs={'game': game, 'obs_type': obs_type, 'frameskip': 4, 
                            'repeat_action_probability': prob, 
                            'player_a': player_a, 'player_b': player_b, 
                            'start_level': start_level,  
                            'difficulty': difficulty,},
                    max_episode_steps=100000,
                    nondeterministic=nondeterministic,
                )

                # No frameskip. This means keep every frame.
                register(
                    id='{}-NoFrameskip-v4'.format(name)+ str(i),
                    entry_point='gym_streets_of_rage.envs:SorEnv',
                    kwargs={'game': game, 'obs_type': obs_type, 'frameskip': 1, 
                            'repeat_action_probability': prob,
                            'player_a': player_a, 'player_b': player_b, 
                            'start_level': start_level, 
                            'difficulty': difficulty,},
                    max_episode_steps=100000,
                    nondeterministic=nondeterministic,
                )
                
        
