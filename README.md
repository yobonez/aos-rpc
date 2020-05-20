# Ace of Spades discord rich presence ![GitHub issues](https://img.shields.io/github/issues/yobonez/aos-rpc?style=flat) ![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/yobonez/aos-rpc)

Discord rich presence made for Ace of Spades. Works with both versions 0.75 and 0.76. I'm not planning to make OpenSpades or other clients support.

Requires python 3.4+ with pip

`If you don't want to bother with python i've added an exe at releases page.
If you've already downloaded an exe, then well. That's all. You just need to run it.`

## Preview

![image](https://dl.dropboxusercontent.com/s/35skyr71axafbzp/7oRE0bWOEa.png) ![image](https://dl.dropboxusercontent.com/s/v7xr9y1ggs4iyq8/Discord_t6nweOi0TR.png)

![image](https://dl.dropboxusercontent.com/s/174c7e27hnocoda/oeT2EQyf8A.png) ![image](https://dl.dropboxusercontent.com/s/xgkn919tr5nsbmk/Discord_mYVnwJVZUi.png)

![image](https://dl.dropboxusercontent.com/s/ehms7uh7txq4gbc/SNmyXVOehZ.png)

## Instalation & running

+ Clone my repository `>git clone https://github.com/yobonez/aos-rpc.git`
+ Install requirements `>pip install -r requirements.txt`
+ Run `>python rpc.py`

### Run in background

+ Option 1: For exe file use `Option 3`, but only with "Program/script" and "Start in" (for logs) parameter or just run manually
+ Option 2: Run it manually in background `>pythonw rpc.py`
+ Option 3: Use task scheduler
  + Add task
  + Set it to trigger on login
  + Action (start a program):
    + Program/script: (path to `pythonw.exe` interpreter)
    + Add arguments: (path to `rpc.py` script)
    + Start in: (path to folder with `rpc.py` in it)
    + Save task settings and run

## TODO's

+ Detect if player actually joined the game (already choosed team and weapon etc.)
+ Make code less cancer and sphagetti
+ Make it more readable
