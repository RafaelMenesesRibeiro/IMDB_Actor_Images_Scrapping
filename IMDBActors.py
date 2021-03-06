import os, time, errno
import urllib.request, urllib3
import requests, json
from bs4 import BeautifulSoup

#-------------------------------------------------------------------------------

	#TO BE FILLED BY THE USER

#-------------------------------------------------------------------------------
IMAGES_TO_DONWLOAD = 100 #Number of images to download. MUST BE A MULTIPLE OF 50.


#-------------------------------------------------------------------------------

	#MAIN STRUCTURES AND VARIABLES

#-------------------------------------------------------------------------------
BASE_URL = 'http://www.imdb.com/search/name?gender=male,female&ref_=nv_cel_m_3&start=1'
BASE_ID_URL = 'http://www.imdb.com/xml/find?json=1&nr=1&nm=on&q='
MOVIE_COLABORATION_URL = 'http://www.imdb.com/search/title?title_type=feature&roles='


#-------------------------------------------------------------------------------

	#FUNCTIONS

#-------------------------------------------------------------------------------
def downloadActors():
	initTime = time.time()
	count = 0
	for i in range(1, IMAGES_TO_DONWLOAD, 50):
		url = BASE_URL.replace('&start=1', '&start={}'.format(i))
		print('Downloading page {} of {}...'.format(int((i-1) / 50 + 1), int(IMAGES_TO_DONWLOAD/50)))
		response = http.request('GET', url)
		soup = BeautifulSoup(response.data, 'lxml')
		table = soup.find('table', attrs={'class':'results'})
		t = time.time()
		for row in table.find_all("tr")[1:]:
			tds = row.find_all('td')
			#Gets the actor's image.
			imageLink = tds[1].find_all('img')[0]
			imageURL = imageLink.get('src')
			url = imageURL.replace('._SX54', '_UX214')
			url = url.replace('._SY74', '_UY317')
			url = url.replace(',54', ',214')
			url = url.replace(',74', ',317')
			#Gets the actor's name.
			actorDescription = tds[2].get_text().splitlines()
			actorName = actorDescription[1]
			#Download the actor's image.
			try:
				localPath = os.path.join(PATH, '{}.jpg'.format(actorName))
				urllib.request.urlretrieve(url, localPath)
				count += 1
			except:
				print('Couldn\'t save image.')
		print('Took {} seconds to download page {}.'.format(int(time.time() - t), int((i-1) / 50 + 1)))
	endTime = time.time()
	print('\nProgram took {} seconds to download {} images.'.format(int(endTime - initTime), count))
	print('Done.')

def getActorID(actorName):
	nameURL = actorName.replace(' ', '+')
	u = BASE_ID_URL + nameURL
	response = requests.get(u)
	respT = json.loads(response.text)
	actorID = respT['name_popular'][0]['id']
	return actorID

def getActorsMovies(actorIDList):
	actorsMovies = []
	url = MOVIE_COLABORATION_URL + ','.join(actorIDList)
	response = http.request('GET', url)
	soup = BeautifulSoup(response.data, 'lxml')
	movieList = soup.find('div', attrs={'class':'lister-list'})
	h3s = movieList.find_all('h3')
	for i in h3s:
		movieTitle = i.find_all('a')[0].contents[0]
		print(movieTitle)
		actorsMovies.append(movieTitle)
	return actorsMovies


#-------------------------------------------------------------------------------

	#CODE EXECUTION

#-------------------------------------------------------------------------------
if __name__ == '__main__':
	try:
		currentDir = os.path.dirname(os.path.realpath(__file__))
		PATH = os.path.join(currentDir, 'actors')
		os.makedirs(PATH)
	except OSError as e:
		if e.errno != errno.EEXIST:
			print('Could not create folder in where to store the images.')
			print('Create a folder with the name "actors" in the directory of the script file.')
			raise
	
	http = urllib3.PoolManager()
	downloadActors();