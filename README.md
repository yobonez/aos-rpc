# Ace of Spades discord rich presence ![GitHub issues](https://img.shields.io/github/issues/yobonez/aos-rpc?style=flat)

Discord rich presence made for Ace of Spades. Works with both versions 0.75 and 0.76. I'm not planning to make OpenSpades or other clients support.

Requires python 3.4+ with pip

## Preview

![image](https://dl.dropboxusercontent.com/s/35skyr71axafbzp/7oRE0bWOEa.png) ![image](https://dl.dropboxusercontent.com/s/v7xr9y1ggs4iyq8/Discord_t6nweOi0TR.png)

![image](https://dl.dropboxusercontent.com/s/174c7e27hnocoda/oeT2EQyf8A.png) ![image](https://dl.dropboxusercontent.com/s/xgkn919tr5nsbmk/Discord_mYVnwJVZUi.png)

![image](https://dl.dropboxusercontent.com/s/ehms7uh7txq4gbc/SNmyXVOehZ.png)

## Instalation & running

+ Clone my repository `>git clone https://github.com/yobonez/aos-rpc.git`
+ Install requirements `>pip install -r requirements.txt`
+ Run `>python presence.py`

### Run in background

+ Option 1: Run it manually in background `>pythonw presence.py`
+ Option 2: Use task manager
  + Add task
  + Set it to trigger on login
  + Action (start a program):
    + Program/script: (path to `pythonw.exe` interpreter)
    + Add arguments: (path to `presence.py` script)
    + Start in: (path to repo folder with `presence.py` in it)
    + Save task settings and run

## TODO's

+ Detect if player actually joined the game (already choosed team and weapon etc.)
+ Make code less cancer and sphagetti
+ Make it more readable
