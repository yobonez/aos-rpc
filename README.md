# Ace of Spades discord rich presence ![GitHub issues](https://img.shields.io/github/issues/yobonez/aos-rpc?style=flat) ![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/yobonez/aos-rpc) ![GitHub All Releases](https://img.shields.io/github/downloads/yobonez/aos-rpc/total?label=Downloads)

Discord rich presence made for Ace of Spades. Works with both versions 0.75 and 0.76. I'm not planning to support OpenSpades or other clients of AoS.

Requires python 3.4+ with pip

Ready to run exe file compiled with pyinstaller is at [releases](https://github.com/yobonez/aos-rpc/releases) page.
If you've already downloaded an exe, then well, that's all. You just need to run it.

## Preview

![image](https://dl.dropboxusercontent.com/s/35skyr71axafbzp/7oRE0bWOEa.png) ![image](https://dl.dropboxusercontent.com/s/v7xr9y1ggs4iyq8/Discord_t6nweOi0TR.png)

![image](https://dl.dropboxusercontent.com/s/qn3bqc94305iiry/8ZBnt13L2C.png) ![image](https://dl.dropboxusercontent.com/s/xgkn919tr5nsbmk/Discord_mYVnwJVZUi.png)

![image](https://dl.dropboxusercontent.com/s/7o7dywhh4122p4t/mQc65N66ib.png)

![image](https://dl.dropboxusercontent.com/s/medrz5xu9luxtyw/rLN71cWSFy.png)

![image](https://dl.dropboxusercontent.com/s/04q2noum2v6fxzz/j1Bsb8yF8c.png)

## Instalation & running

+ Clone my repository `git clone https://github.com/yobonez/aos-rpc.git`
+ Install requirements `pip install -r requirements.txt`
+ Run `python rpc.py`

### Run in background

+ Option 1: For exe file use `Option 3`, but only with "Program/script" and "Start in" (to set where logs will be placed) parameter or just run manually
+ Option 2: Run it manually in background `pythonw rpc.py`
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
