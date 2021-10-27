'''
For now i will not be including per round stats just the fight totals,
I'll save this step as a potential future improvement on the model 

notes:

'''

#imports 
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

# file = open('ufcData.csv', 'wb')
# writer = csv.writer(file)
# writer.writerow([Fighter, Knockdown, Significant Strikes Thrown, Significant Strikes Landed, Total Stirkes, Takedown Attempts, Takedown Percentage, Submissions Attacked, Reversal, Control Time])

#soup object for list of fight cards 
source = requests.get("http://ufcstats.com/statistics/events/completed?page=all").text
soup = BeautifulSoup(source, 'lxml')

#find all table rows with links to fight statistics
# for link in soup.find_all("a", class_="b-link b-link_style_black"):
# 	print(link)

link = soup.find("a", class_="b-link b-link_style_black")
if link.has_attr('href'):
# 	#print(link['href'])
	pass

#soup object for each fight card
fightCardPage = requests.get(link['href']).text
fightCardSoup = BeautifulSoup(fightCardPage, 'lxml')

dataLink = fightCardSoup.find("a", class_="b-flag b-flag_style_green")
if dataLink.has_attr('href'):
	#print(dataLink['href'])
	pass

#soup object for fight statistics
fightStatPage = requests.get(dataLink['href']).text
fightStatSoup = BeautifulSoup(fightStatPage, 'lxml')

#return match details 
method = fightStatSoup.find("i", class_="b-fight-details__text-item_first").contents[3].get_text().strip()
details = fightStatSoup.find("i", class_="b-fight-details__text-item")
roundNumEnd = details.get_text()
timeEnd = details.next_sibling.next_sibling.get_text()
timeFormat = details.next_sibling.next_sibling.next_sibling.next_sibling.get_text()

#getting a series with the values that we want
s1 = pd.Series([roundNumEnd, timeEnd, timeFormat])
s1 = s1.astype(str)
s1 = s1.str.strip(' \n')
s1 = s1.str.split('\n').str.get(2)
s2 = pd.Series([method])
s = s1.append(s2, ignore_index=True)

df1 = pd.DataFrame(s)
# print(df1)

#return fights statistics 
table = fightStatSoup.tbody.tr
rows = []
for stats in table.children:
	row = []
	for p in stats:
		try:
			row.append(p.text.replace('\n', ''))
		except:
			continue
	if len(row) > 0:
		rows.append(row)

df2 = pd.DataFrame(rows[1:], columns = rows[0])
print(df2)

#switch into 1 single row 

#add column to get name

# file.close()





