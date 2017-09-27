# IMDB_Downloader

Script to download the faces of all the actors in IMDB

## Requirements
* urlib3 and urlib.request
* requests
* json
* BeautifulSoup (from bs4)

## How To Use
```python
#Set IMAGES_TO_DONWLOAD in IMDBActors.py:11 to the number of images to be downloaded.
IMAGES_TO_DONWLOAD = 100 #Number of images to download. MUST BE A MULTIPLE OF 50. 
```

```bash
#Run the script to download the images. The images will be donwloaded to a folder with
#the name 'actors' created by the script in the same directory.
$ python IMDBActors.py
```
