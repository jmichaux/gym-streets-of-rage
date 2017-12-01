# gym-streets-of-rage
Gym Streets of Rage is an environment bundle for OpenAI Gym built on top of the [Retro Learning Environment](https://github.com/nadavbh12/Retro-Learning-Environment).

## Installation

#### Dependencies

## Streets of Rage

#### Environment addresses

| Environment Settings    | RAM Address | Values   |
| ----------------------- | ----------- | ------   |
| Set Level               |   0xFF02    | 1-8      |
| Set Difficulty          |   0xFFC6    | 1-4      |
| Set Number of Continues |   0xFF1B    |  0       |
| Select Player 1         |   0XB858    |  0-2 (Adam, Axel, Blaze)|
| Current Level           |   0xFC42    |          |
| Boss health             |   0xB933    |          |

#### Terminal States

A terminal state is reached whenever an agent runs out of lives or reaches the end of the current level

| Level | 0xB810 | 0xFCCE |
| ----- |  ----  | ----   |
|   1   |        |        |
|   2   |        |        |
|   3   |        |        |
|   4   |        |        |
|   5   |        |        |
|   6   |        |        |
|   7   |        |        |
|   8   |        |        |

#### Agent Addresses

|      Agent         |   RAM Address  |
|   ---------        |  ------------  |
| Player 1 Character |     0XB858     |
| Player 1 Points    | 0xFF08, 0xFF0A |
| Player 1 Health    |     0xB832     |
| Player 1 Lives     |     0xFF20     |  
| Player 1 Continues |     0xFF1B     |
| Player 1 Kills     |                |


## Streets of Rage 2


#### Environment addresses

| Environment Settings    | RAM Address | Values |
| ----------------------- | ----------- | ------ |
| Set Level               |   0xFD0E    |   1-8  |
| Set Difficulty          |   0xFD04    |  1-6   |
| Set Number of Continues |   0xFD06    |   0    |
| Select Player 1         |             |        |
| Current Level           |   0xFC42    |        |

#### Terminal States

A terminal state is reached whenever an agent runs out of health and lives: 

|        | RAM Address | Values |
| -----  |  ----       | ----   |
| Health |   0xEF80    |  0     |
| Lives  |   0XEF82    |  0     |

A terminal state is also reached whenever an agent reaches the end of a specified level:

| Level | 0xFC44  | 0xFCCE |
| ----- |  ----   | ----   |
|   1   |   0     |  12    |
|   2   |   0     |  12    |
|   3   |   0     |  16    |
|   4   |   0     |  22    |
|   5   |   0     |  10    |
|   6   |   0     |  10    |
|   7   |   0     |  18    |
|   8   |   0     |  10    |


#### Agent Addresses

|  Agent Attributes  |   RAM Address  | Hexidecimal  | Decimal |
|   ---------        |  ------------  | -------------| --------|
| Player 1 Character |                |              |         |
| Player 1 Points    | 0xEF99, 0xEF96 |              |         |
| Player 1 Health    |     0xEFA8     |              |         |
| Player 1 Lives     |     0xEF82     |              |         |
| Player 1 Continues |                |              |         |
| Player 1 Kills     |     0xEF4D     |              |         |


## Streets of Rage 3

#### Environment addresses

| Environment Settings    | RAM Address | Values |
| ----------------------- | ----------- | ------ |
| Set Level               |   0xFD0E    |        |
| Set Difficulty          |   0xFD04    |        |
| Set Number of Continues |   0xFD06    |        |
| Select Player 1         |             |        |
| Current Level           |   0xFC42    |        |
| Time remaining          |             |        |

#### Terminal States

A terminal state is reached whenever an agent runs out of lives or reaches the end of the current level

| Level | 0xFC44 | 0xFCCE |
| ----- |  ----  | ----   |
|   1   |        |        |
|   2   |        |        |
|   3   |        |        |
|   4   |        |        |
|   5   |        |        |
|   6   |        |        |
|   7   |        |        |
|   8   |        |        |

#### Agent Addresses

|                    |   RAM Address  | Hexidecimal  | Decimal |
|   ---------        |  ------------  | -------------| --------|
| Player 1 Character |                |              |         |
| Player 1 Points    | 0xEF99, 0xEF96 |              |         |
| Player 1 Health    |     0xEFA8     |              |         |
| Player 1 Lives     |     0xEF82     |              |         |
| Player 1 Continues |                |              |         |
| Player 1 Kills     |     0xEF4D     |              |         |
