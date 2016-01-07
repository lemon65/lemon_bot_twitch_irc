#!/usr/bin/python

import os
import sys
import time
import pickle
import requests
import twitch_irc_bot as bot_main

CHAN = sys.argv[1]

# List viewers in a channel
def list_viewers():
    try:
        channel = CHAN.strip('#')
        data = requests.get('https://tmi.twitch.tv/group/user/%s/chatters' % channel).json()
        viewers = data['chatters']['viewers']
        mods = data['chatters']['moderators']
        mega_list = viewers + mods
    except Exception:
        return None
    return mega_list

# Save the dict Object
def save_obj(dict, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(dict, f, pickle.HIGHEST_PROTOCOL)

# Load the pickle Object
def load_obj(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

# function appends data to the file
def add_xp(user_list):
    file_path = './bot_files/%s_chan_xp.pkl' % CHAN.strip('#')
    file_bool = os.path.isfile(file_path)
    if not file_bool:
        data_dict = {}
    else:
        data_dict = load_obj(file_path)
    for user_step in user_list:
        if user_step not in data_dict.keys():
            bot_main.message('Welcome %s to the Channel' % user_step)
            data_dict[user_step] = 10
        else:
            data_dict[user_step] = data_dict[user_step] + 10 
    save_obj(data_dict, file_path)
    return

def main():
    file_bool = os.path.exists("./bot_files")
    if not file_bool:
        os.system('mkdir ./bot_files')
    while True:
        user_list = []
        pre_count = list_viewers()
        time.sleep(60)
        post_count = list_viewers()
        if pre_count and post_count:
            for pre_step in pre_count:
                if pre_step in post_count:
                    user_list.append(pre_step)
        if user_list:
            add_xp(user_list)


if __name__ == "__main__":
    sys.exit(main())
