import random
import requests
import pandas as pd
import discord
import os
from dotenv import load_dotenv

# Load bot token
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Set Intents(permissions) and initialize Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Print to terminal when bot connected
@client.event
async def on_ready():
    print('bot is locked and loaded')

# Trigger the bot with 'aram+'
@client.event
async def on_message(message):
    # Check if the message is from the bot
    if message.author == client.user:
        return

    if message.content.startswith('aram+'):
        # champion info load
        url = 'https://ddragon.leagueoflegends.com/cdn/12.18.1/data/en_US/champion.json'
        req2 = requests.get(url)

        champ_ls = list(req2.json()['data'].keys())

        champ_df = pd.DataFrame()
        for i in range(len(champ_ls)):
            pre_df = pd.json_normalize(req2.json()['data'][champ_ls[i]])
            champ_df = pd.concat([champ_df, pre_df])
        
        # User input
        await message.channel.send('What role would you like? (Case sensitive, one role only)')

        all_roles = ['Tank', 'Support', 'Marksman', 'Fighter', 'Mage']
        
        # Check if user input is a valid role
        def check(m):
            return m.content in all_roles

        # msg is user input from role prompt, 20s timeout
        msg = await client.wait_for('message', check=check, timeout=20)
        await message.channel.send(msg.content + 's coming right up')

        # Create champ pool based on matching tags with role
        role = []
        role.append(msg.content)
        champ_pool = []
        # If role is empty, go to else
        if role:
            for j in range(len(champ_ls)):
                this_champ = req2.json()['data'][champ_ls[j]]
                if any(x in this_champ['tags'] for x in role):
                    champ_pool.append(this_champ['name'])
        else:
            champ_pool = list(champ_df['name'])

        #print("This is the current champ pool:", champ_pool, "\n")

        # Choose champs for team 1 then team 2
        pool_size = 10
        team1 = random.sample(champ_pool, pool_size)
        team2 = random.sample(list(set(champ_pool) - set(team1)), pool_size)

        #print('Champion pool for Team 1:', team1)
        #print('Champion pool for Team 2:', team2)

        # Tell your friends because we made it
        await message.channel.send('Champion pool for Team 1')
        await message.channel.send(team1)
        await message.channel.send('Champion pool for Team 2')
        await message.channel.send(team2)

client.run(TOKEN)