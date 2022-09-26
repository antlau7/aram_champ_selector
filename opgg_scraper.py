import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://na.op.gg/modes/aram"
session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
html = session.get(url).content
soup = BeautifulSoup(html, "html.parser")
table1 = soup.find('table')

# Obtain every title of columns with tag <th>
headers = []
for i in table1.find_all('th'):
    title = i.text
    headers.append(title)
print(headers)

# Create and fill data frame with table rows
mydata = pd.DataFrame(columns=headers)
for j in table1.find_all('tr')[1:]:
    row_data = j.find_all('td')
    row = [i.text for i in row_data]
    length = len(mydata)
    mydata.loc[length] = row

mydata.to_csv('mydata.csv', index=True)

# Choose tier and create champ pool
tier = [1, 2, 3, 4, 5]
pool_list = {}
champ_pool = pd.DataFrame()
for i in range(len(tier)):
    pool_list[i] = mydata[mydata['Tier'] == str(tier[i])]
    champ_pool = pd.concat([champ_pool, pool_list[i]])

print("This is the current champion pool:\n", champ_pool)

pool_size = 10
team1 = champ_pool.sample(n=pool_size)
team2 = pd.concat([champ_pool, team1]).drop_duplicates(keep=False).sample(n=pool_size)

print("This is the pool for Team 1:\n", team1)
print("This is the pool for Team 2:\n", team2)
