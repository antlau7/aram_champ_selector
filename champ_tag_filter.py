import random
import requests
import pandas as pd

# champion info load
url = 'https://ddragon.leagueoflegends.com/cdn/12.18.1/data/en_US/champion.json'
req2 = requests.get(url)

champ_ls = list(req2.json()['data'].keys())

champ_df = pd.DataFrame()
for i in range(len(champ_ls)):
    pre_df = pd.json_normalize(req2.json()['data'][champ_ls[i]])
    champ_df = pd.concat([champ_df, pre_df])

# Create champ pool based on matching tags with role
role = ['Tank', 'Support']
champ_pool = []
# If role is empty, go to else
if role:
    for j in range(len(champ_ls)):
        this_champ = req2.json()['data'][champ_ls[j]]
        if any(x in this_champ['tags'] for x in role):
            champ_pool.append(this_champ['name'])
else:
    champ_pool = list(champ_df['name'])

print("This is the current champ pool:", champ_pool, "\n")

# Choose champs for team 1 then team 2
pool_size = 10
team1 = random.sample(champ_pool, pool_size)
team2 = random.sample(list(set(champ_pool) - set(team1)), pool_size)

print('Champion pool for Team 1:', team1)
print('Champion pool for Team 2:', team2)
