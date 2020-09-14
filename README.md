# Chatcraft
Chat with Your Minecraft Server Through Discord!

## Intro
My friends and I wanted to play some minecraft, but it was hard to keep track of what went on in game and seeing who was online. So I created a discord bot that can be integrated into a Discord text channel that would relay the ingame chat to the channel and messages from the channel to the server.

**WARNING: This bot runs without any support for plugins/mods, which means the discord bot has to directly interact with your server console. This could pose a problem exposing your console.**
## Requirements
* Linux
* [A vanilla Minecraft server](https://www.minecraft.net/en-us/download/server) (probably also works on a modded server)
* Install [Python 3.6+](https://www.python.org/downloads/)
* Install [Discord.py](https://pypi.org/project/discord.py/)
* Install [GNU Screen](https://www.gnu.org/software/screen/)
*  Get a[Discord API key](https://discord.com/developers/docs/intro)
* Check Cron Status
## Installation 
```
# git clone into your server root folder
git clone https://github.com/Vrandus/Chatcraft.git

# Run chatcraft.py using screen or normally

python3.6 chatcraft.py

screen -S bot -d -m python3.6 chatcraft.py

```
*You can find some more useful scripts [here](https://github.com/Vrandus/Chatcraft/tree/master/useful%20scripts)*
