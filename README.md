#Polybar Nba Boxscore Module

A small python script to show nba latest boxscore:

![](./images/screen.png)

## Usage

Install requirements.txt with pip.(Either python3 or virtual env.)

Add a module to call this python script into your polybar config:
```
[module/nba]
type = custom/script
exec = .config/polybar/modules/nba-boxscore/launch.sh
label = %output%
interval = 10
```

In the launch.sh specify your python path, I use virtual env:

```
#!/bin/bash
source .config/polybar/modules/nba-boxscore/venv/bin/activate
# virtualenv is now active.
#
python .config/polybar/modules/nba-boxscore/nba-boxscore.py
```
