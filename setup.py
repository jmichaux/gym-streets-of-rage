from setuptools import setup

setup(name='gym_streets_of_rage',
      version='0.0.1',
      description='Gym User Env - Every level of the original Streets of Rage triology',
      url='https://github.com/jmichaux/gym-streets-of-rage',
      author='Jonathan Michaux',
      author_email='jmichaux@ttic.edu', 
      install_requires=['gym>=0.2.3',
                        'rle_python_interface>=1.1.5', 'PyOpenGL']
)
