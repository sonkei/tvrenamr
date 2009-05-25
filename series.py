import logging
import urllib
import xml.etree.ElementTree as ET

class Series:
    apikey = 'C4C424B4E9137AFD'
    url = "http://www.thetvdb.com/api/"
    get_series = "GetSeries.php?seriesname="
    name = ""
    
    def __init__(self, series_name):
        self.name = series_name.lower()
        
    def getSeriesId(self):
        logging.debug('Retrieving series ID: %s', self.name)
        f = urllib.urlopen(self.url + self.get_series + self.name)
        dom = ET.fromstring(f.read())
        if dom == None: raise Exception('Error retriving XML for for: '+ self.name)
        for series in dom.findall("Series"):
            s = series.find("SeriesName").text
            if s.lower() == self.name.lower():
                self.name = s
                return series.find("seriesid").text
        
    def getEpisodeName(self, series_id, season, episode):
        logging.info('Retrieving episode name for: '+ self.name)
        episode_url = self.url + self.apikey +"/series/"+ series_id +"/default/"+ season +"/"+ str(int(episode)) +"/en.xml"
        f = urllib.urlopen(episode_url)
        dom = ET.fromstring(f.read())
        if dom != None: return dom.find("Episode").find("EpisodeName").text
        else: raise Exception('Episode not found: '+ self.name + " - " + season + episode)