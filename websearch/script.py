import urllib.parse
from bs4 import BeautifulSoup
from .utils import get

class WebSearch :

    def __init__(self, query) :
        self.query = query

    @property
    def images(self):
        """ 
        Une fonction qui récupère toutes les liens des images 
        resultats selon les mot-clé en paramètre.
        """
        result = []
        url = 'https://fr.images.search.yahoo.com/search/images;_ylt=AwrJS5dMFghcBh4AgWpjAQx.;_ylu=X3oDMTE0aDRlcHI2BGNvbG8DaXIyBHBvcwMxBHZ0aWQDQjY1NjlfMQRzZWMDcGl2cw--?p='+urllib.parse.quote(self.query)+'&fr2=piv-web&fr=yfp-t-905-s'
        requete = get(url)
        soup = BeautifulSoup(requete.text, 'html.parser')
        container = soup.find("ul", {"id":"sres"})
        try :
            lis = container.find_all('li')
        except :
            return result
        if len(lis)==0 : 
            return result
        for li in lis:
            img = li.find("img")
            img = str(img["data-src"]).split("&pid")
            result.append(str(img[0]))  

        return result 

    @property
    def pages(self):    
        """
        Une fonction qui récupère toutes les liens des  
        resultats selon les mot-clé en paramètre.
        """
        result = []
        url = "https://www.google.com/search?client=firefox-b-d&q=" + urllib.parse.quote(self.query)
        requete = get(url)
        soup = BeautifulSoup(requete.text, 'html.parser')
        a = soup.find_all("a")
        for link in a :
            tmp = link["href"][7:-1].split('&')
            if tmp[0].startswith('http'):
                result.append(urllib.parse.unquote(tmp[0]))
        return result

