import urllib.parse
from bs4 import BeautifulSoup
from utils import *

class Image :
    """
    Une classe qui va récupérer les liens de résultat 
    d'une recherche de google.
    """
    
    def __init__(self) :
        self.source = 'www.yahoo.com'
    
    @classmethod
    def search(self, query):
        """ 
        Une fonction qui récupère toutes les liens des images 
        resultats selon les mot-clé en paramètre.
        """
        result = []
        url = 'https://fr.images.search.yahoo.com/search/images;_ylt=AwrJS5dMFghcBh4AgWpjAQx.;_ylu=X3oDMTE0aDRlcHI2BGNvbG8DaXIyBHBvcwMxBHZ0aWQDQjY1NjlfMQRzZWMDcGl2cw--?p='+urllib.parse.quote(query)+'&fr2=piv-web&fr=yfp-t-905-s'
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

if __name__ == "main":
    print("")
