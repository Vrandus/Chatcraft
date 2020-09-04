import discord
import io
import os
import threading
import time
client = discord.Client()

queue = []
def chat_listener(channel):
    path = "../logs/latest.log"
    current = open(path, "r")
    print("file opened")
    print(channel.id)
    minecraft_channel = client.get_channel(channel.id)
    while 1:
        time.sleep(0.5)
        str = current.readline()
        if "[Server]" not in str:
            if "<" and ">" in str:
                minecraft_channel.send(content="bruh")

    current.close()

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))
    perm_channel = discord.TextChannel
    for channel in client.get_all_channels():
        if channel.name == "buildtogether":
            perm_channel = channel

    x = threading.Thread(target=chat_listener, args=(perm_channel,),  daemon=True)
    x.start()

@client.event
async def on_message(message):
    if message.author == client.user or message.channel.name != "buildtogether":
        return
    command = f'screen -S mcserver -p 0 -X stuff "say [{message.author}] {message.content} ^M"'
    os.system(command)
    # if message.content.startswith('$hello'):
    #     await message.channel.send('Hello!')

token = ""
with open('token.txt', 'r') as file:
     token = file.readline()
     file.close()

client.run(token)
