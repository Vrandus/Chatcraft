import discord
import io
import os
import threading
import time
import asyncio
client = discord.Client()

queue = []
def chat_listener(channel):
    path = "../logs/latest.log"
    current = open(path, "r")
    print("file opened")
    print(channel.id)
    minecraft_channel = client.get_channel(channel.id)
    while 1:
        time.sleep(0.1)
        str = current.readline()
        if "[Server]" not in str:
            if "<" and ">" in str:

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(send_message(minecraft_channel, str))
                loop.close()
                print(str)
                # minecraft_channel.send(content=str)


    current.close()
async def send_message(channel, message):
    await channel.send(message)
@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))
    perm_channel = discord.TextChannel
    print(channel_name)
    for channel in client.get_all_channels():
        if channel.name == channel_name:
            perm_channel = channel

    x = threading.Thread(target=chat_listener, args=(perm_channel,),  daemon=True)
    x.start()

@client.event
async def on_message(message):
    if message.author == client.user or message.channel.name != channel_name:
        return
    command = f'screen -S mcserver -p 0 -X stuff "say [{message.author}] {message.content} ^M"'
    os.system(command)
    # if message.content.startswith('$hello'):
    #     await message.channel.send('Hello!')

token = ""
channel_name = ""
with open('bot.properties', 'r') as file:
    channel_name = file.readline()
    channel_name = channel_name[channel_name.index("=")+1: -1]
    print(channel_name)

    token = file.readline()
    token = token[token.index("=")+1:]
    print(token)

    file.close()

client.run(token)
