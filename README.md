# twitch_irc_bot
##This is a repo for an IRC bot for twitch.tv
###please download as you see fit and if possible credit --> lemon65
- Twitch - http://www.twitch.tv/lemon65
- Community-Website --> http://home.ramcommunity.com/
- Download with -->   git clone https://github.com/lemon65/twitch_irc_bot

###**Dependencies ->**
```
sudo pip install configparser  
```

###**Setup ->**
* You will need to edit the "user_config.ini" with you bot connection information and if needed all the channels that it should join. the Channels are not something that you have to config but you can setup the script to join and track X number of channels. 
```
[twitch_bot_configs]

HOST = irc.twitch.tv
PORT = 6667
NICK = <BOT_NAME>
PASS = <BOT_AUTH_CODE>

[channels_to_join]

CHANNEL1 = <CHANNEL1>
CHANNEL2 = <CHANNEL2>
```

###**User Commands ->**

* '!xp' -- shows the users current XP
* '!robot' -- pulls data from a local file and sends that to the chat (Jokes / Funny)
* '!yomama target_person' -- pulls a yomama joke from (http://api.yomomma.info/) and presents it as <target><joke>
* '!battle target_person' -- gathers a random pokemon attack and formats it as <user> attacks <target> with <attack>
* '!help' -- displays the github readme file

###**USER-Command Spam Control ->** 
* Bot has a built in timeout, so each user can only send one command per 60 seconds

###**Admin Commands ->**
* '!toggle' -- Turns off all commands for the channel, note the XP counter is still running.

###**Credit To -- >** 
  * Lemon65 and my father -- > "know alot about a little and a little about a lot" -- David (2013)
