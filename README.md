# zilliqastats
Python script to gather stats from Zilliqa mining logs

Assuming you followed the ZIlliqa mining setup guide here: https://github.com/Zilliqa/Zilliqa/wiki/Mining

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
