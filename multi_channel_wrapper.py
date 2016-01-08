#!/usr/bin/python
# simple python wrapper to luanch the the to join channels

import sys
import configparser
import subprocess as sp

# --------------------------------------------- Read Config Files -----------------------------------------------
config = configparser.ConfigParser()
config.read('./user_config.ini')
CHANNELS = config['channels_to_join']
# ---------------------------------------------------------------------------------------------------------------

def main():
    for channel_step in CHANNELS:
        target_channel = config['channels_to_join'][channel_step]
        command = 'python twitch_irc_bot.py %s' % target_channel
        sp.Popen(command.split(),stdout = sp.PIPE,stderr = sp.PIPE, shell=False)
if __name__ == "__main__":
    sys.exit(main())

