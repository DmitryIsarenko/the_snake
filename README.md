# Snake Game with Dynamic Objects

A classic snake game implemented with **pygame**, enhanced with dynamic game objects such as **apples** and **rocks** that interact with the player and game logic. The game architecture uses object-oriented design with mixins to separate responsibilities.

---
##  Features

-  Apples:
  - Spawn at random positions.
  - Have a limited lifespan and blink before disappearing.
  - Collect to increase snake length and speed.

-  Rocks:
  - Spawn at random positions.
  - Have a limited lifespan and blink before disappearing.
  - Act as obstacles on the field.
  - Cause game over on collision.

-  Snake:
  - Increases in length and speed with each apple.
  - Dies when colliding with a rock or itself.
  - Warps on the opposite side on reaching game field edge.


---
## Customization

You can tweak game parameters at the top of the file `the_snake.py`:
- `START_SPEED`: Snake starting speed. (Ticks per second).
- `SPEED_STEP`: Snake speed increase step per apple. (Ticks per second).
- `APPLE_LIFE_IN_TICKS`: Range of lifespan for apples.
- `APPLE_BLINK_SPEED_IN_TICKS`: How fast apple blinks before vanishing.
- `ROCKS_GENERATED`: Amount of rocks on the field simultaneously.
- `ROCK_LIFE_IN_TICKS`: Range of lifespan for rock.
- `ROCK_BLINK_SPEED_IN_TICKS`: How fast apple blinks before vanishing.
- etc...


## Requirements

- Python 3.12
- pygame==2.6.1


---
## Run the game from terminal:

### Windows

```bash
py -3.12 -m venv venv
```
  
```bash
source venv/Scripts/activate
```

```bash
pip install -r requirements.txt
```
  
```bash
python the_snake.py
```


### MacOS / Linux

```bash
python3 -m venv venv
```
  
```bash
venv/bin/activate
```

```bash
pip install -r requirements.txt
```
  
```bash
python3 the_snake.py
```

---
## Create executable:

### Windows

```bash
py -3.12 -m venv venv
```
  
```bash
source venv/Scripts/activate
```

```bash
pip install -r requirements.txt
```
  
```bash
pyinstaller the_snake.py --clean --noconfirm --onefile
```

### MacOS / Linux

```bash
python3 -m venv venv
```
  
```bash
venv/bin/activate
```

```bash
pip install -r requirements.txt
```
  
```bash
pyinstaller the_snake.py --clean --noconfirm --onefile
```


---
## TODO:

- Add apples counter to GUI
- Add "games played" counter to GUI


---
# Authors:

Developed by:
	Yandex.Practicum team,
	Dmitry Isarenko.
---