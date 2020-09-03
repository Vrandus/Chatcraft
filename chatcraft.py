import discord
import io

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

token = ""
with open('token', 'r') as file:
     token = file.readline()
     file.close()

client.run(token)
