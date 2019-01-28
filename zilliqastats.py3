#!/usr/bin/env python3
#################################################################################
#										#
# Purpose: Python script to gather some stats surrounding Zilliqa mining	#
#										#
# Script : zilliqastats.py3							#
# Version : 1.4									#
# Date : 28-01-2019								#
# Author : therealmko								#
#										#
# Version	Date		Major changes					#
# 0.1		28-12-2018	Initial inception				#
# 1.0		30-12-2018	First OK version				#
# 1.1		04-01-2019	Added zilliqa stats option			#
# 1.2           07-01-2019      Some small performance improvements		#
# 1.3		09-01-2019	Fixed bug related to try statement reading file	#
# 1.4           28-01-2019      Changed POW searches to match latest build      #
#										#
# To Do (if I get around to it):						#
#										#
# Notes:									#
#										#
#################################################################################

import sys
import argparse
import subprocess
import re
import time
from datetime import datetime
import os.path

# Function to parse the provided inputs and make them available throughout the rest of the script
def cli_options():
   cli_args = {}
   cli_args['option'] = 'total'
   cli_args['logname'] = 'zilliqa-00001-log.txt'

   # Parse the CLI
   parser = argparse.ArgumentParser()
   parser.add_argument('-o', '--option', help='Amount of Zilliqa rewarded or show Epoch stats, options: total, daytotal or epochstats', default='total')
   parser.add_argument('-l', '--logname', help='Zilliqa log to check rewards from', default='zilliqa-00001-log.txt')

   # Parse arguments and die if error
   try:
      args = parser.parse_args()
   except Exception:
      sys.exit(2)

   # Assign and verify commandline arguments
   if args.option:
      cli_args['option'] = args.option
      if cli_args['option'] not in ['total', 'daytotal', 'epochstats']:
         print(('ERROR: Invalid option "' + cli_args['option'] + '" provided.'))
         print(('Please run "' + sys.argv[0] + ' -h" to see valid options.')) 
         sys.exit(2)
   if args.logname:
      cli_args['logname'] = args.logname
      if not os.path.isfile(cli_args['logname']):
         print(('ERROR: ' + cli_args['logname'] + ' does not exist.'))
         print(('Please run "' + sys.argv[0] + ' -h" to see valid options.'))
         sys.exit(2)

   return (cli_args)


# Function to parse the logs for Zilliwa rewards and return usefull stuff
def zilliqa_log_parsing_reward(logname, search_string):
   # Read zilliqa logfile and search for rewards
   with open(logname, "r", encoding="ISO-8859-1") as file:
      match_list = []
      for line in file:
         if re.search(search_string, line):
             match_list.append(line)
   file.close

   # Split strings found containing rewards into variables 
   return_rewards = [] 
 
   for item in range(0, len(match_list)):
      data_string, reward_string = match_list[item].rsplit(']', 1)

      data = data_string.split(']')
      timestamp = data[2].lstrip('[').replace('T', ' ')
      epoch = data[4].lstrip('[')
      reward = reward_string.split()[1]

      return_rewards.append([timestamp, epoch, reward])
      
   return return_rewards


# Function to print total amount of Zilliqa rewards as found in the logs
def zilliqa_total(return_rewards, logname):
   total = 0
   
   for item in return_rewards:
      total = total + float(item[2])

   total_rewards = total / 10**12

   print(("\nTotal amount of Zilliqa received as reward, captured by " + logname + ": " + str(total_rewards) + "\n"))


# Function to print total amount of Zilliqa earned per day as found in the logs
def zilliqa_daytotal(return_rewards, logname):
   # Set some initial values used in this function
   reward_date_list = []
   reward_date_old = ''
   total = 0

   # Loop over all rewards, add those belonging to same date and store in list to nicely print at the end
   for item in return_rewards:
      reward_date = item[0].split()[0]

      if reward_date == reward_date_old or reward_date_old == '':
         total = total + float(item[2])
      else:
         reward_date_list.append([reward_date_old, total / 10**12])
         total = float(item[2])

      # Store processed date in temp variable to check against in if
      reward_date_old = reward_date

   # Capture final date in log as it won't fall into else anymore
   reward_date_list.append([reward_date_old, total / 10**12])

   # Print results
   print(("\nAmount of Zilliqa received per day as reward, captured by " + logname + ":"))

   for reward_date, reward_total in reward_date_list:
      print(("Reward on " + reward_date + ": " + str(reward_total)))

   print("\n")


def zilliqa_epoch_stats(logname, search_string_reward_received, search_string_reward_not_received, search_string_pow, search_string_backup_member):
# Set some initial values used in this function
   match_list = []
   match_reward_received = ''
   match_reward_not_received = ''
   match_pow = ''
   match_backup_member = ''

# Read zilliqa logfile and search for reward stats
   with open(logname, "r", encoding="ISO-8859-1") as file:
      for line in file:
         if re.search(search_string_reward_received, line):
             match_reward_received = line
         elif re.search(search_string_reward_not_received, line):
             match_reward_not_received = line
         elif re.search(search_string_pow, line):
             match_pow = line
         elif re.search(search_string_backup_member, line):
             match_backup_member = line

         if match_reward_received != '' or match_reward_not_received != '' and match_pow != '' and match_backup_member != '':
            if match_reward_received != '':
               match_reward = match_reward_received
            else:
               match_reward = match_reward_not_received

            match_list.append([match_reward, match_pow, match_backup_member])
            match_reward_received = ''
            match_reward_not_received = ''
            match_pow = ''
            match_backup_member = ''

   file.close

   return match_list


# Function to run main script
def main():
   # Set some parameters
   search_string_reward_received = '\[REWARD\]\ Got'
   search_string_reward_not_received = 'Got no reward this ds epoch'
   search_string_pow = 'Storing DS Block Number'
   search_string_backup_member = 'I am backup member'

   # Parse the CLI options
   (cli_parms) = cli_options()

   # Check if I am already running and exit
   if int(subprocess.check_output('ps x | grep \'' + sys.argv[0] + '\' | grep -cv grep', shell=True)) > 1:
      sys.exit(0)

   # Call function for option requested
   if cli_parms['option'] == 'total':
      # Parse Zilliqa log to get rewards out
      return_rewards = zilliqa_log_parsing_reward(cli_parms['logname'], search_string_reward_received)
      zilliqa_total(return_rewards, cli_parms['logname'])
   elif cli_parms['option'] == 'daytotal':
      # Parse Zilliqa log to get rewards out
      return_rewards = zilliqa_log_parsing_reward(cli_parms['logname'], search_string_reward_received)
      zilliqa_daytotal(return_rewards, cli_parms['logname']);
   elif cli_parms['option'] == 'epochstats':
      # Call stats gathering
      epoch_stats = zilliqa_epoch_stats(cli_parms['logname'], search_string_reward_received, search_string_reward_not_received, search_string_pow, search_string_backup_member)
 
      for epoch_reward, epoch_pow, epoch_backup_member in epoch_stats:
         print((epoch_pow + epoch_backup_member + epoch_reward + '\n'))


if __name__ == "__main__":
   main()
