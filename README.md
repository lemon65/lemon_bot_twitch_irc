#Repository for Lemon Bot - Twitch.tv IRC Bot
###please download as you see fit and if possible credit --> lemon65
- Twitch - http://www.twitch.tv/lemon65
- Community-Website --> http://home.ramcommunity.com/
- Download with -->   git clone https://github.com/lemon65/twitch_irc_bot
- Created with a Raspberry PI -- https://www.raspberrypi.org/

###**Dependencies -> Python v2.7.9 **
```
sudo pip install configparser  
```

###**Setup ->**
* You will need to edit the "user_config.ini" with you bot connection information and if you would like all the channels it should join.
```
[twitch_bot_configs]

# IRC Server Address
HOST = irc.twitch.tv
# IRC Server Port
PORT = 6667
# Bot NickName
NICK = BOTNAME
# Twitch.tv auth code -- https://twitchapps.com/tmi/
PASS = AUTHCODE
# Seconds between user commands -- NEEDS TO BE AN INT -- > 30,60,90
SPAM = 30
# Cost in xp for a raffle ticket
RAFFLE_COST = 1000

[channels_to_join]

CHANNEL1 = <CHANNEL1>
CHANNEL2 = <CHANNEL2>
```

###**Running the BOT ->**
```
Single Channel JOIN -- >   python twitch_irc_bot.py <TARGET_CHANNEL>
Multi Channel JOIN --> python multi_channel_wrapper.py
    (This gets Channel names from the "user_config.ini")
```

###**User Commands ->**

* '!xp' -- shows the users current XP
* '!robot' -- pulls data from a local file and sends that to the chat (Jokes / Funny)
* '!yomama target_person' -- pulls a yomama joke from (http://api.yomomma.info/) and presents it as target joke
* '!battle target_person' -- gathers a random pokemon attack and formats it as user attacks target with attack
* '!raffle' -- Buy a Raffle Ticket for the user, define the cost in the user_config.ini.
* '!display' -- show the user the number of raffle tickets.
* '!enter' -- will consume one raffle ticket and enter them into a raffle.
* '!help' -- displays the github readme file.

###**USER-Command Spam Control ->** 
* Bot has a built in timeout, so each user can only send one command per X-seconds. Config this in the user_config.ini

###**Admin Commands ->**
* '!toggle' -- Turns off all commands for the channel, note the XP counter is still running.
* '!draw' -- picks a random user for the raffle winner.
* '!clear' -- clear all the users from the raffle, NOTE -- if the bot is shut off the current user in the raffle will be lost.

###**Credit To -- >** 
  * Lemon65 and my father -- > "know alot about a little and a little about a lot" -- David (2013)
