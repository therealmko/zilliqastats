# zilliqastats
Python script to gather stats from Zilliqa mining logs

Assuming you followed the Zilliqa mining setup guide here: https://github.com/Zilliqa/Zilliqa/wiki/Mining

There are 2 script versions. One if you have Python version < 3 (default Ubuntu 16.04). The other if you have Python 3.x (default Ubuntu 18.04). Use:
- Python 2.7 -> zilliqastats.py
- Python 3.x -> zilliqastats.py3


Copy or clone the zilliqastats.py into your "join" directory.

$ ./zilliqastats.py -h
usage: zilliqastats.py [-h] [-o OPTION] [-l LOGNAME]

optional arguments:
  -h, --help            show this help message and exit
  -o OPTION, --option OPTION
                        Amount of Zilliqa rewarded or show Epoch stats,
                        options: total, daytotal or epochstats
  -l LOGNAME, --logname LOGNAME
                        Zilliqa log to check rewards from
