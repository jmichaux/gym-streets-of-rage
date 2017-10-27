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


class Sor2Env(gym.Env, utils.EzPickle):
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, obs_type='ram', frameskip=(2, 5), repeat_action_probability=0.25, character='Axel', difficulty=1, num_lives=3, level=3):
        """
				Frameskip should be either a tuple (indicating a random range to
        choose from, with the top value exclude), or an int.

				character = 'axel' ,'blaze', 'max', 'skate'
				difficulty = 'very_easy', 'easy', 'normal', 'hard', 'hardest', 'mania'
				level = 1-8 
				num_lives = 1-9
				"""

        utils.EzPickle.__init__(self, obs_type)
        assert obs_type in ('ram', 'image')
				
        self.game_path = self.get_rom_path('streets_of_rage_2')

        self._obs_type = obs_type
        self.frameskip = frameskip
        self.rle = rle_python_interface.RLEInterface()
        self.viewer = None
        self.character = character
        self.difficulty = difficulty
        self.num_lives = num_lives
        self.level = level

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
        self.rle.setString(b'SOR2_player_1_character', self.character.encode('utf-8'))
        self.rle.setInt(b'SOR2_difficulty', self.difficulty)
        self.rle.setInt(b'SOR2_lives', self.num_lives)
        self.rle.setInt(b'SOR2_start_level', self.level)
        self.rle.setInt(b'SOR2_end_level', self.level)
        return


    def get_rom_path(self, game):
        cwd = os.path.dirname(__file__)
        roms_path = os.path.join(cwd, 'roms')
        for file in os.listdir(roms_path):
            if fnmatch.fnmatch(file, game + '*'):
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

    def _step(self, a):
        reward = 0.0
        action = self._action_set[a]

        if isinstance(self.frameskip, int):
            num_steps = self.frameskip
        else:
            num_steps = self.np_random.randint(self.frameskip[0], self.frameskip[1])
        for _ in range(num_steps):
            reward += self.rle.act(action)
        ob = self._get_obs()

        return ob, reward, self.rle.game_over(), {}

    def _get_image(self):
        self.rle.getScreenRGB(self._buffer)
        if self.screen_width == 640:
            return np.repeat(self._buffer[:, :, [0, 1, 2]], 2, axis=0) 
        else:
            return self._buffer[:, :, [0, 1, 2]]

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
