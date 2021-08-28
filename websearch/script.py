import urllib.parse
from bs4 import BeautifulSoup
from requests import get, head

class WebSearch :
    '''
        Classe permettant de prendre les différents lien sur le web.
    '''
    _headers =  {'User-Agent': 'Googlebot/2.1 (http://www.googlebot.com/bot.html)'}

    def __init__(self, query) :
        self.query = query
        # utiliser pour l'optimisation
        self.__data = {}

    def __verif_content(self, urls, doc='pdf'):
        '''
            Verification du bon format du lien
        '''
        new_urls = []
        for url in urls:
            # Envoie d'une requete qui recupere que l'en tête.
            rq = head(url).headers
            # Verfier si le lien renvoie bien le format voulu.
            if rq.get('content-type') == f'application/{doc}':
                new_urls.append(url)
        # renvoyer les urls verfiés.
        return new_urls
        
    @property
    def images(self):
        """ 
        Une fonction qui récupère toutes les liens des images 
        resultats selon les mot-clé en paramètre.
        """
        #  On verifie que les resultats n'est pas deja enregistrer.
        if self.__data.get('images'):
            if self.__data['images'][0] == self.query:
                return self.__data['images'][1]
        result = []
        url = 'https://fr.images.search.yahoo.com/search/images;_ylt=AwrJS5dMFghcBh4AgWpjAQx.;_ylu=X3oDMTE0aDRlcHI2BGNvbG8DaXIyBHBvcwMxBHZ0aWQDQjY1NjlfMQRzZWMDcGl2cw--?p='+urllib.parse.quote(self.query)+'&fr2=piv-web&fr=yfp-t-905-s'
        requete = get(url, headers=self._headers, timeout=10)
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
        #  Sauvegarde des resultats pour optimiser la prochaine même appel.
        self.__data['images'] = (self.query, result)
        return result 

    @property
    def pages(self):    
        """
        Une fonction qui récupère toutes les liens des  
        resultats selon les mot-clé en paramètre.
        """
        #  On verifie que les resultats n'est pas deja enregistrer.
        if self.__data.get('pages'):
            if self.__data['pages'][0] == self.query:
                return self.__data['pages'][1]
        result = []
        url = "https://www.google.com/search?client=firefox-b-d&q=" + urllib.parse.quote(self.query)
        requete = get(url, headers=self._headers, timeout=10)
        soup = BeautifulSoup(requete.text, 'html.parser')
        a = soup.find_all("a")
        for link in a :
            tmp = link["href"][7:-1].split('&')
            if tmp[0].startswith('http'):
                result.append(urllib.parse.unquote(tmp[0]))
        #  Sauvegarde des resultats pour optimiser la prochaine même appel.
        self.__data['pages'] = (self.query, result)
        ''' On enleve les deux liens non necessaire à la fin du liste
            -> https://support.google.com/websearch?p=...
            -> https://accounts.google.com/ServiceLogin?continue=...
        '''
        return result[:-2]
    
    @property
    def pdf(self):
        '''
            Fonction pour recuperer que les pdf.
        '''
         #  On verifie que les resultats n'est pas deja enregistrer.
        if self.__data.get('pdf'):
            if self.__data['pdf'][0] == self.query:
                return self.__data['pdf'][1]
        tmp = self.query
        self.query = 'filetype:pdf ' + self.query
        result = self.__verif_content(self.pages, 'pdf')
        self.query = tmp
         #  Sauvegarde des resultats pour optimiser la prochaine même appel.
        self.__data['pdf'] = (self.query, result)
        return result
