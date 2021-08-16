import urllib.parse
from bs4 import BeautifulSoup
from utils import *

class WebSearch :
    """
    Une classe qui va récupérer les liens de résultat 
    d'une recherche de google.
    """
    def __init__(self) :
        self.source = 'www.google.com'

    def google(self,keywords):    
        """
        Une fonction qui récupère toutes les liens des  
        resultats selon les mot-clé en paramètre.
        """
        result = []
        url = "https://www.google.com/search?client=firefox-b-d&q=" + urllib.parse.quote(keywords)

        soup = get(url)
        a = soup.find_all("a")

        for link in a :
            result.append(link["href"])

        return result
if __name__ == "main":
    web = WebSearch()
    x= web.google("Je suis malade")
    print("a")
    print(x)


