import discord
import io
import os
import threading
import time
import asyncio


client = discord.Client()


def between_listener(loop, channel):
    # loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(chat_listener(channel))
    loop.close()
async def chat_listener(channel):
    path = "../logs/latest.log"
    current = open(path, "r")
    print("file opened")
    print(channel.id)
    minecraft_channel = client.get_channel(channel.id)
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    while 1:
        # time.sleep(0.1)
        str = current.readline()
        if "[Server]" not in str:
            if "<" and ">" in str:
                
                await send_message(minecraft_channel, str)

                # loop = asyncio.new_event_loop()
                # loop.run_until_complete(send_message(minecraft_channel, str))

                
                print(str)
                # minecraft_channel.send(content=str)
        try:
            await client.wait_for('message', timeout=0.1)
        except:
            # print("DEBUG: no new messages")
            continue 
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
            await perm_channel.send("Bot initialized")
    loop = client.loop
    x = threading.Thread(target=between_listener, args=(loop, perm_channel,),  daemon=True)
    x.start()
    
    

@client.event
async def on_message(message):
    if message.author == client.user or message.channel.name != channel_name:
        return
    
    command = f'screen -S mcserver -p 0 -X stuff "say [{message.author}] {message.content} ^M"'

    os.system(command)


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

