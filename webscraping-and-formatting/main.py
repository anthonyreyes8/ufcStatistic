'''
For now i will not be including per round stats just the fight totals,
I'll save this step as a potential future improvement on the model 

notes:
might need to make another scraper for the 

'''
import requests
from bs4 import BeautifulSoup
import dataframeEditor as de 
import pandas as pd

#For creating new beautiful soup objects from the links
def createSoupFromLink(link):
	try:
		if link is not None:
			linkForNewSoup = requests.get(link).text
			newSoup = BeautifulSoup(linkForNewSoup, 'lxml')
			return newSoup
	except AttributeError:
		print("Error with the href thingy")

def getStatistics(linkToStatistics):
	soup = createSoupFromLink(linkToStatistics)
	fd_df = de.fightDetails_df(soup)
	fs_df = de.fightStatistics_df(soup)
	#merging the dataframes
	df = fd_df.join(fs_df)
	return df

#Returns the links to each fight so that statistics can be scraped
def getCard(linkToCard):
	soup = createSoupFromLink(linkToCard)
	#there is another table on the next page
	table =	soup.find("tbody")
	rows = table.find_all("tr")
	frames = []
	for row in rows:
		link = row.find("a")
		statistics = getStatistics(link)
		#statistics returns the single df now I need to combine all of them
		frames.append(statistics)

	#from the list of dataframes we can merge them all together
	df = pd.concat(frames)
	return df

#Loop through each ufc event returning the statistics for each card
def getEventStatistics(soupObject):
	table = soupObject.find("tbody")
	a_tag = table.find_all("a", class_="b-link b-link_style_black", href=True)
	frames = []
	for a in a_tag:
		if a.has_attr('href'):
			linkToCard = a['href']
			fightCard_df = getCard(linkToCard)
			frames.append(fightCard_df)
	
	#Dataframe for all fight cards is the concationation of all of the dataframes
	master_df = pd.concat(frames)
	return master_df

#main function	
def main():
	#setting up the soup object
	StatisticsSource = requests.get("http://ufcstats.com/statistics/events/completed?page=all").text
	StatisticsSoup = BeautifulSoup(StatisticsSource, 'lxml')
	getEventStatistics(StatisticsSoup)
	master_dataframe = getEventStatistics(StatisticsSoup)
	master_dataframe.to_csv()

if __name__ == "__main__":
	main()





