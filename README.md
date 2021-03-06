# Ace of Spades discord rich presence  ![GitHub All Releases](https://img.shields.io/github/downloads/yobonez/aos-rpc/total?label=Downloads) ![GitHub issues](https://img.shields.io/github/issues/yobonez/aos-rpc?style=flat)

Discord rich presence made for classic client of Ace of Spades 0.75/76. I'm not planning to support OpenSpades or other clients of AoS.

Ready to run exe file compiled using pyinstaller is at [releases](https://github.com/yobonez/aos-rpc/releases) page.

Requires python 3.4+

## Preview

![image](https://dl.dropboxusercontent.com/s/35skyr71axafbzp/7oRE0bWOEa.png) ![image](https://dl.dropboxusercontent.com/s/v7xr9y1ggs4iyq8/Discord_t6nweOi0TR.png)

![image](https://dl.dropboxusercontent.com/s/qn3bqc94305iiry/8ZBnt13L2C.png) ![image](https://dl.dropboxusercontent.com/s/xgkn919tr5nsbmk/Discord_mYVnwJVZUi.png)

![image](https://dl.dropboxusercontent.com/s/7o7dywhh4122p4t/mQc65N66ib.png) ![image](https://dl.dropboxusercontent.com/s/04q2noum2v6fxzz/j1Bsb8yF8c.png)

![image](https://dl.dropboxusercontent.com/s/medrz5xu9luxtyw/rLN71cWSFy.png) ![image](https://dl.dropboxusercontent.com/s/gj24es6zvmf7m7y/4zic3YUBHD.png)

## Instalation & running

+ Clone my repository `git clone https://github.com/yobonez/aos-rpc.git`
+ Install requirements `pip install -r requirements.txt`
+ Run `python rpc.py`

### Run in background

+ Option 1: For exe file use `Option 3`, but in addition to "Program/script" parameter, add a path to a folder that will store logs in "Start in" parameter
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

+ [ ] Detect if player actually joined the game (already choosed team and weapon etc.)
+ [ ] Make code more readable
