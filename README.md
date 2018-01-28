# gym-sor
Gym Streets of Rage is an environment bundle for OpenAI Gym built on top of the [Retro Learning Environment](https://github.com/nadavbh12/Retro-Learning-Environment). Users can train one or two agents on any single level of Streets of Rage 1-3.  Users

## Installation
First install the Retro Learning Environment:
```bash
git clone https://github.com/jmichaux/Retro-Learning-Environment.git
cd Retro-Learning-Environment
pip install .
```
Next, install gym_streets_of_rage:
```bash
git clone https://github.com/jmichaux/gym-streets-of-rage.git
cd gym-streets-of-rage
pip install .
```
## Choosing an Environment
To choose an environment for training a single agent, use the following pattern: game-character-level-difficulty
```python
env = gym.make('streets_of_rage_ii-max-1-4-v0')
```

## Rewards
By default, the environment returns a dictionary of rewards corresponding to: health, lives, points, kills

## TODO
- set rewards
- re-map the action space
- Fix two player 

## Acknowledgements
- [@nadavbh12](https://github.com/nadavbh12) for his work on RLE.
- [@gsaurus](https://github.com/gsaurus) for his work hacking and reverse engineering the Streets of Rage series.
