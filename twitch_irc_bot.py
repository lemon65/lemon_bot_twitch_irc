#!/usr/bin/python
# IRC Bot for Twitch

import os
import re
import sys
import json
import time
import random
import socket
import bot_xp
import requests
import configparser
import subprocess as sp
from oauth_bot_lemon import Auth

# -- TODO - Top five Xp holders

get_auth = Auth()
auth_code = get_auth.send_auth()

# --------------------------------------------- Read Config Files -----------------------------------------------
config = configparser.ConfigParser()
config.read('./user_config.ini')
HOST = str(config['twitch_bot_configs']['HOST'])
PORT = int(config['twitch_bot_configs']['PORT'])
NICK = str(config['twitch_bot_configs']['NICK'])
SPAM = str(config['twitch_bot_configs']['SPAM'])
PASS = auth_code

# --------------------------------------------- Global Bools ----------------------------------------------------
try:
    CHAN = "#" + sys.argv[1]
except:
    print 'You need to add a Channel[python <FileName.py> <Channel_Name>]'
    sys.exit(1)

TOGGLE_BOOL = True
RECENT_USERS = {}
CURRENT_RAFFLE = []

# Create the Obj for Connection to the Server
IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IRC.connect((HOST, PORT))
IRC.send('PASS ' + PASS + '\r\n')
IRC.send('NICK ' + NICK + '\r\n')
IRC.send('USER ' + NICK + '\r\n')
IRC.send('JOIN ' + CHAN + '\r\n')
    
XP_FILE = './bot_files/%s_chan_xp.pkl' % CHAN.strip('#')
RAFFLE_FILE = './bot_files/%s_raffle_tickets.pkl' % CHAN.strip('#')
# ---------------------------------------------------------------------------------------------------------------

# Function to Send a message
def message(data):
    # PRIVMSG #channel :Message to send
    IRC.send("PRIVMSG " + CHAN + " :" + data + "\r\n")
    return

# Say that the Bot has left the channel
def part():
    message('MrDestructoid Bot Leaving: %s' % CHAN)
    IRC.send("PART " + CHAN)
    return

# Say that the Bot has joined the Channel
def join():
    message('MrDestructoid Bot_Lemon Has Joined: %s' % CHAN)
    return

# Strip and return User Name
def get_user_name(line_data):
    user = norm_data(line_data.split(' ')[0],':', '')
    return user

# Get mods for the Channel
def get_mods():
    loop_bool = True
    while loop_bool:
        try:
            channel = CHAN.strip('#')
            data = requests.get('https://tmi.twitch.tv/group/user/%s/chatters' % channel).json()
            mods = data['chatters']['moderators']
        except Exception:
            print 'Got an API Error, setting mods list to empty'
            mods = []
            continue
        if mods:
            time.sleep(1)
            loop_bool = False
    print('Mods Found from API - %s' % mods)
    return mods


# Take the chat line data and call the correct command or function
def dispatcher(line_data):
    global TOGGLE_BOOL
    user = get_user_name(line_data)
    line_data = line_data.lower()
    message = norm_data(line_data.split(':')[-1],'', '')
    if message == '!help' and TOGGLE_BOOL:
        display_help()
    if message == '!raffle' and TOGGLE_BOOL:
        buy_ticket(user)
    if message == '!display' and TOGGLE_BOOL:
        display_tickets(user)
    if message == '!enter' and TOGGLE_BOOL:
        enter_the_raffle(user)
    if message == '!xp' and TOGGLE_BOOL:
        command_get_user_xp(user)
    if message == '!robot' and TOGGLE_BOOL:
        command_robot()
    if '!yomama' in message and TOGGLE_BOOL:
        target_patteren = '^!yomama (\w+)'
        target = re.search(target_patteren, message)
        if target:
            yo_mama_so_fat(target.group(1))
    if '!battle' in message and TOGGLE_BOOL:
        target_patteren = '^!battle (\w+)'
        target = re.search(target_patteren, message)
        if target:
            pokemon_battle(user, target.group(1))
    if message == '!toggle':
        mods_list = get_mods()
        if user in mods_list:
            if TOGGLE_BOOL:
                print 'system offline, set by %s' % user
                TOGGLE_BOOL = False
            else:
                print 'system online, set by %s' % user
                TOGGLE_BOOL = True
    if message == '!draw':
        mods_list = get_mods()
        if user in mods_list:
            draw()
    if message == '!clear':
        mods_list = get_mods()
        if user in mods_list:
            clear_raffle()
    return

# Return Robot's response
def command_robot():
    robot_data = './bot_files/things_to_say.txt'
    with open(robot_data, 'rb') as f:
        data = f.read().split('\n')
        del data[-1]
    formatted_data = data[random.randint(0, len(data))]
    message(str(formatted_data))
    return

#Battle time!
def pokemon_battle(user, target):
    attacks_data = './bot_files/pokemon_attacks.txt'
    with open(attacks_data, 'rb') as f:
        data = f.read().split('\n')
        del data[-1]
    attack = data[random.randint(0, len(data))]
    message('%s Attacked %s with %s' % (user, target, attack))
    return

# Pull data from an API and send it to the user
def yo_mama_so_fat(target):
    try:
        json_data = requests.get('http://api.yomomma.info/').json()
    except Exception:
        message('%s, Insert Mean Yo Mama Joke HERE' % target)
        return
    message('%s %s' % (target, json_data['joke']))
    return

# Print Help to the User
def display_help():
    message('https://github.com/lemon65/twitch_irc_bot/blob/master/README.md')
    return

# get the requested user XP
def command_get_user_xp(user):
    data_dict = bot_xp.load_obj(XP_FILE)
    if not data_dict:
        message('Currently no XP File...')
        return
    try:
        users_xp = data_dict[user]
    except KeyError:
        users_xp = 0
        pass
    message('%s your XP is: %s' % (user, users_xp))
    return

# Start the XP Count
def start_xp_counter():
    command = 'python bot_xp.py %s' % CHAN
    print 'Starting XP Counter...'
    sp.Popen(command.split(),stdout = sp.PIPE,stderr = sp.PIPE, shell=False)
    return

# Enter Raffle
def enter_the_raffle(user):
    global CURRENT_RAFFLE
    raffle_dict = bot_xp.load_obj(RAFFLE_FILE)
    if not raffle_dict:
        raffle_dict = {}
    if user in raffle_dict.keys():
        if raffle_dict[user] >= 1:
            CURRENT_RAFFLE.append(user)
            raffle_dict[user] = raffle_dict[user] - 1
            message('%s has joined the Raffle!' % user)
            bot_xp.save_obj(raffle_dict, RAFFLE_FILE)
        else:
            message('%s has no raffle tickets' % user)
            return
    else:
        message('%s has no raffle tickets' % user)
        return
    return

# Clear the give away
def clear_raffle():
    global CURRENT_RAFFLE
    CURRENT_RAFFLE = []
    return

# draw a user from the pool
def draw():
    if len(CURRENT_RAFFLE) > 1:
        rand_target = random.randint(0, len(CURRENT_RAFFLE))
        message('%s Has won the Raffle!' % CURRENT_RAFFLE[rand_target])
    else:
        message('We need to wait for more people!')
    return

# Function to display Tickets
def display_tickets(user):
    raffle_dict = bot_xp.load_obj(RAFFLE_FILE)
    if not raffle_dict:
        message('Currently no users have raffle tickets')
        return
    message('%s Has %s Raffle Tickets' % (user, raffle_dict[user]))
    return

# Function to buy a raffle ticket
def buy_ticket(user):
    xp_dict = bot_xp.load_obj(XP_FILE)
    raffle_dict = bot_xp.load_obj(RAFFLE_FILE)
    try:
        if not raffle_dict:
            raffle_dict = {}
        if xp_dict[user] >= 1000:
            xp_dict[user] = xp_dict[user] - 1000
            if user in raffle_dict.keys():
                raffle_dict[user] = raffle_dict[user] + 1
            else:
                raffle_dict[user] = 1
            message('Thats 1000xp, enjoy your raffle ticket![Current Count: %s]' % raffle_dict[user])
            bot_xp.save_obj(xp_dict, XP_FILE)
            bot_xp.save_obj(raffle_dict, RAFFLE_FILE)
        else:
            message('Raffle Tickets cost 1000xp, you only have %s' % xp_dict[user])
    except Exception:
        pass
    return

# Function to strip data
def norm_data(input_data, bad_data, replace):
    bad_list = ['\r', '\n', bad_data]
    for bad_step in bad_list:
        input_data = input_data.replace(bad_step, replace)
    return input_data

def main():
    join()
    start_xp_counter()
    while True:
        try:
            response = IRC.recv(1024).decode("utf-8")
            if 'PING :tmi.twitch.tv' in response:
                IRC.send('PONG tmi.twitch.tv\r\n')
            else:
                data =  norm_data(response, '', '')
                patteren = '!.*@.*.tmi.twitch.tv PRIVMSG '
                line_data = re.sub(patteren, ' - ', data)
                dispatcher(line_data)
        except KeyboardInterrupt:
            part()
            break

if __name__ == "__main__":
    sys.exit(main())
