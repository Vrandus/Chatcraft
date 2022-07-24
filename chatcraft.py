from cmath import log
from hashlib import new
import time
import discord
import io
import os
import threading
import json
import asyncio
import emoji
import logging
import sys
client = discord.Client()
client_loop = client.loop
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("latest.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)
keywords_death = {"shot", "pummeled", "death", "escape", 
    "drowned", "up", "killed", "hit", "fell", "squashed",
    "flames", "walked", "fighting", "went", "swim", "lightning",
     "lava", "slain", "fireballed", "suffocated", "squished",
      "impaled", "live", "withered", "died" "obliterated",
      "sonically-charged", "crisp", "skewered", "froze", "bang"}

prev_file_length = 0
def between_listener(channel):
    new_loop = asyncio.new_event_loop()
    
    new_loop.run_until_complete(minecraft_messages_listener(channel))
    new_loop.close()

def load_uuids():
    with open('./UUID.json', 'r') as f:
        uuids = json.load(f)
        return uuids

def save_uuids(uuids):
    with open('./UUID.json', 'w') as f:
        json.dump(uuids, f, indent=4)

async def minecraft_messages_listener(channel):
    logger = logging.getLogger(__name__)
    path = logPath + "latest.log"
    log_file = open(path, "r")
    global prev_file_length


    current_file_length = sum(1 for line in open(path))
    for i in range(prev_file_length):
        log_file.readline()
    UUID = load_uuids()
    logger.info("Listening to minecraft log %s", path)
    minecraft_channel = client.get_channel(channel.id)
    while 1:
        try:
            current_file_length = sum(1 for line in open(path))
            server_log_file = open(path, 'r')
            for i in range(prev_file_length):
                server_log_file.readline()
            for i in range(current_file_length - prev_file_length):
                str = server_log_file.readline()
                # Checks if server is up or down
                if "[Server thread/INFO]: Done" in str and ")! For help, type \"help\"" in str:
                    logger.info("Detected server startup")
                    embedded = discord.Embed(title="Server is Up!", colour=discord.Colour.green(), type="rich")
                    handle_minecraft_message(minecraft_channel, embedded) 
                if "[Server thread/INFO]: Stopping server" in str:
                    logger.info("Detected server shutdown")
                    embedded = discord.Embed(title="Server is Down!", colour=discord.Colour.red(), type="rich")
                    handle_minecraft_message(minecraft_channel, embedded) 
                
                # Gets UUID of player
                if "[User Authenticator #" in str and "/INFO]: UUID of player" in str:
                    split_str = str.split()
                    UUID[split_str[7]] = split_str[9]
                    save_uuids(UUID)

                # Checks if server someone joined or left the game
                if ("<" not in str and ">" not in str) and ("joined the game" in str or "left the game" in str):
                    split_str = str.split()
                    if "joined" in str:
                        embedded = discord.Embed(title=str[33:], colour=discord.Colour.green(), type="rich")
                    else:
                        embedded = discord.Embed(title=str[33:], colour=discord.Colour.greyple(), type="rich")
                    
                    if split_str[3] in UUID.keys():
                        url = f'https://crafatar.com/avatars/{UUID[split_str[3]]}?size=24'
                        logger.info(url)
                        embedded.set_thumbnail(url=url)
                    handle_minecraft_message(minecraft_channel, embedded)

                # Checks if player action
                if "<Server>" not in str and "[Server thread/INFO]: /" not in str:
                    # Checks if player message
                    if "<" in str and ">" in str and "<null>" not in str:
                        str = str[33:]
                        handle_minecraft_message(minecraft_channel, str)
                    # Checks if player kill
                    elif "ServerLevel" not in str:
                        split_str = str.split()
                        check_death = set(split_str)
                        if len(check_death & keywords_death) >= 1:
                            embedded = discord.Embed(title=str[33:], colour=discord.Colour.red(), type="rich")
                            if split_str[3] in UUID.keys():
                                url = f'https://crafatar.com/avatars/{UUID[split_str[3]]}?size=24'
                                embedded.set_thumbnail(url=url)
                            handle_minecraft_message(minecraft_channel, embedded)
            prev_file_length = current_file_length
            server_log_file.close()
        except:
            continue
       
    prev_file_length = current_file_length
    asyncio.sleep(0.05)
    log_file.close()


def handle_minecraft_message(minecraft_channel, str):
    handle_minecraft_message = asyncio.run_coroutine_threadsafe(send_message(minecraft_channel, str), client_loop)
    handle_minecraft_message.result()



async def send_message(channel, message):
    if type(message) is discord.Embed:
        logger.info("sending out embedded message %s", message)
        await channel.send(embed=message)
    else:
        logger.info("sending out message %s", message)
        await channel.send(message)

@client.event
async def on_ready():
    logger.info('logged in as %s', client.user.name)
    perm_channel = discord.TextChannel
    
    logger.info("Listening to Channel %s", channel_name)
    await client.change_presence(activity=discord.Game(name=ip))
    for channel in client.get_all_channels():
        if channel.name == channel_name:
            perm_channel = channel
    global prev_file_length
    path = logPath + "latest.log"

    prev_file_length = sum(1 for line in open(path))
    loop = client.loop
    x = threading.Thread(target=between_listener, args=(perm_channel,))
    x.start()
    
    

@client.event
async def on_message(message):
    if message.author == client.user or message.channel.name != channel_name:
        return
    
    # print(emoji.demojize(message.content))
    if len(message.attachments) > 0:
        message.content = message.content +": Uploaded Attachment"
    command = f'screen -S mcserver -p 0 -X stuff "say <{message.author}> {emoji.demojize(message.content)} ^M"'

    os.system(command)



f = open('config.json')
config = json.load(f)
channel_name = config['channel']
ip = config['ip']
logPath = config['logPath']
token = os.environ.get('DISCORD_TOKEN')


client.run(token)

