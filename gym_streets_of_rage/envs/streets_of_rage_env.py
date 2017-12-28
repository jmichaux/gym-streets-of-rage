import numpy as np
import os
import gym
import fnmatch
from gym import error, spaces
from gym import utils
from gym.utils import seeding

try:
    from rle_python_interface import rle_python_interface
except ImportError as e:
    raise error.DependencyNotInstalled("{}. (HINT: you can install RLE dependencies by running 'pip install gym[rle]'.)".format(e))

import logging
logger = logging.getLogger(__name__)


#def check_button(action_string, action, value, name, first):
#    if (action & value) > 0:
#        if first:
#            action_string += name
#        else:
#            action_string += ' | ' + name
#
#    return action_string
#
#
#def get_action_meaning(action):
#    action_string = ''
#    first = False
#    action_string = check_button(action_string, action, 0x1, 'B', first)
#    action_string = check_button(action_string, action, 0x2, 'Y', first)
#    action_string = check_button(action_string, action, 0x4, 'SELECT', first)
#    action_string = check_button(action_string, action, 0x8, 'START', first)
#    action_string = check_button(action_string, action, 0x10, 'UP', first)
#    action_string = check_button(action_string, action, 0x20, 'DOWN', first)
#    action_string = check_button(action_string, action, 0x40, 'LEFT', first)
#    action_string = check_button(action_string, action, 0x80, 'RIGHT', first)
#    action_string = check_button(action_string, action, 0x100, 'A', first)
#    action_string = check_button(action_string, action, 0x200, 'X', first)
#    action_string = check_button(action_string, action, 0x400, 'L', first)
#    action_string = check_button(action_string, action, 0x800, 'R', first)
#    action_string = check_button(action_string, action, 0x1000, 'L2', first)
#    action_string = check_button(action_string, action, 0x2000, 'R2', first)
#    action_string = check_button(action_string, action, 0x4000, 'L3', first)
#    action_string = check_button(action_string, action, 0x8000, 'R3', first)
#
#    return action_string


def to_ram(rle):
    ram_size = rle.getRAMSize()
    ram = np.zeros((ram_size),dtype=np.uint8)
    rle.getRAM(ram)
    return ram


class SorEnv(gym.Env, utils.EzPickle):
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, game, obs_type='ram', frameskip=(2, 5), repeat_action_probability=0.25, 
                 difficulty=1, player_a='axel', player_b='', start_level=3):
        """
		Frameskip should be either a tuple (indicating a random range to
        choose from, with the top value exclude), or an int.

        SOR
			character: 'axel' ,'blaze', 'adam'
			difficulty: 1-4
			level = 1-7 
			num_lives = 1, 3, 5, 7

        SOR2
            character: 'axel' ,'blaze', 'skate', 'max'
            difficulty: 1-6
            level = 1-8
            num_lives = 1-9

        SOR3
            character: 'axel' ,'blaze', 'skate', 'zan'
            difficulty: 1-5
            level = 1-8 
            num_lives = 1-9            

		"""
        utils.EzPickle.__init__(self, obs_type)
        assert obs_type in ('ram', 'image')
				
        self.game_path = self.get_rom_path(game)
        print(self.game_path)
        print(game)

        self._obs_type = obs_type
        self.frameskip = frameskip
        self.rle = rle_python_interface.RLEInterface()
        self.viewer = None
        self.player_a = player_a.lower()
        self.player_b = player_b.lower()
        self.num_lives = 3
        self.difficulty = difficulty
        self.start_level = start_level
        self.end_level = start_level
        self.num_agents = self._get_num_agents()


        # Tune (or disable) RLE's action repeat:
        # https://github.com/openai/gym/issues/349
        assert isinstance(repeat_action_probability, (float, int)), "Invalid repeat_action_probability: {!r}".format(repeat_action_probability)
        self.rle.setFloat('repeat_action_probability'.encode('utf-8'), repeat_action_probability)
        self._set_game_settings()
        self._seed()

        (screen_width, screen_height) = 640, 224 #self.rle.getScreenDims()
        self._buffer = np.empty((screen_height, screen_width, 4), dtype=np.uint8)

        self._action_set = self.rle.getMinimalActionSet()
        self.action_space = spaces.Discrete(len(self._action_set))

        self.screen_width = screen_width
        self.screen_height = screen_height
        
        ram_size = self.rle.getRAMSize()
        if self._obs_type == 'ram':
            self.observation_space = spaces.Box(low=np.zeros(ram_size), high=np.zeros(ram_size)+255)
        elif self._obs_type == 'image':
            self.observation_space = spaces.Box(low=0, high=255, shape=(screen_height, screen_width, ))
        else:
            raise error.Error('Unrecognized observation type: {}'.format(self._obs_type))

    def _set_game_settings(self):
        # Might want to change these to be more consistent
        self.rle.setString(b'SOR_player_1_character', self.player_a.encode('utf-8'))
        self.rle.setString(b'SOR_player_2_character', self.player_b.encode('utf-8'))
        self.rle.setInt(b'SOR_difficulty', self.difficulty)
        self.rle.setInt(b'SOR_lives', self.num_lives)
        self.rle.setInt(b'SOR_start_level', self.start_level)
        self.rle.setInt(b'SOR_end_level', self.end_level)
        # self.rle.setInt(b'SOR_round_clear', True)
        # self.rle.setInt(b'SOR_2p_terminal_both_win', False)
        return


    def get_rom_path(self, game):
        cwd = os.path.dirname(__file__)
        roms_path = os.path.join(cwd, 'roms')
        for file in os.listdir(roms_path):
            if fnmatch.fnmatch(file, game + '.bin'):
                return os.path.join(roms_path, file)

    def _seed(self, seed=None):
        self.np_random, seed1 = seeding.np_random(seed)
        # Derive a random seed. This gets passed as a uint, but gets
        # checked as an int elsewhere, so we need to keep it below
        # 2**31.
        seed2 = seeding.hash_seed(seed1 + 1) % 2**31
        # Empirically, we need to seed before loading the ROM.
        self.rle.setInt(b'random_seed', seed2)
        self.rle.loadROM(self.game_path, 'genesis')
        return [seed1, seed2]

    def _step(self, actions):
        reward = 0.0
        if isinstance(self.frameskip, int):
            num_steps = self.frameskip
        else:
            num_steps = self.np_random.randint(self.frameskip[0], self.frameskip[1])
        for _ in range(num_steps):
            reward += self.rle.act(actions)
        ob = self._get_obs()

        return ob, reward, self.rle.game_over(), {}

    def _get_image(self):
        self.rle.getScreenRGB(self._buffer)
        return self._buffer[:, ::2 , [0, 1, 2]]

    def _get_ram(self):
        return to_ram(self.rle)

    @property
    def _n_actions(self):
        return len(self._action_set)

    def _get_obs(self):
        if self._obs_type == 'ram':
            return self._get_ram()
        if self._obs_type == 'image':
            return self._get_image()

    def _reset(self):
        self.rle.reset_game()
        return self._get_obs()

    def _render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return
        img = self._get_image()
        if mode == 'rgb_array':
            return img
        elif mode == 'human':
            from gym.envs.classic_control import rendering
            if self.viewer is None:
                self.viewer = rendering.SimpleImageViewer()
            self.viewer.imshow(img)

    def get_action_meanings(self):
        return [get_action_meaning(i) for i in self._action_set]

    def _get_num_agents(self):
        if self.player_b:
            return 2
        else:
            return 1

    # def get_player_a_rewards(self):
    #     if self.rom in ['streets_of_rage', 'streets_of_rage_2_players']:
    #         points = _get_ram()[]
    #         health = _get_ram()[]
    #         lives = _get_ram()[]
    #         kills = _get_ram()[]
    #         time = _get_ram()[]
    #     else if self.rom in ['streets_of_rage_ii', 'streets_of_rage_ii_2_players']:
    #         points = _get_ram()[]
    #         health = _get_ram()[]
    #         lives = _get_ram()[]
    #         kills = _get_ram()[]
    #         time = _get_ram()[]
    #     else:
    #         points = _get_ram()[] 
    #         health = _get_ram()[]
    #         lives = _get_ram()[]
    #         kills = _get_ram()[]
    #         time = _get_ram()[]
    #     return points, health, lives, kills, time

    # def get_player_b_rewards(self):
    #     if self.rom in ['streets_of_rage', 'streets_of_rage_2_players']:
    #         points = _get_ram()[] 
    #         health = _get_ram()[]
    #         lives = _get_ram()[]
    #         kills = _get_ram()[]
    #         time = _get_ram()[]
    #     else if self.rom in ['streets_of_rage_ii', 'streets_of_rage_ii_2_players']:
    #         points = _get_ram()[]
    #         health = _get_ram()[]
    #         lives = _get_ram()[]
    #         kills = _get_ram()[]
    #         time = _get_ram()[]
    #     else:
    #         points = _get_ram()[]
    #         health = _get_ram()[]
    #         lives = _get_ram()[]
    #         kills = _get_ram()[]
    #         time =  _get_ram()[]
    #     return points, health, lives, kills, time
