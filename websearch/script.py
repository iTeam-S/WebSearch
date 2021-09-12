import urllib.parse
from bs4 import BeautifulSoup
from requests import get, head

class WebSearch :
    '''
        Classe permettant de prendre les différents lien sur le web.
    '''
    _headers =  {'User-Agent': 'Googlebot/2.1 (http://www.googlebot.com/bot.html)'}

    def __init__(self, query, verif=True):
        '''
            query: prend l'expression à rechercher.
            verif: si True, lance une requete à l'url pour valider
                le bon format du résultat, pardefaut à True.
            peut être desactiver en mettant `verif=False` en argument.
        '''
        # verifier si la recherche est de type mutliple.
        if isinstance(query, list):
            self.query = "'"
            self.query += "' OR '".join(query)
            self.query += "'"
        else:
            self.query = query
        # Utiliser pour la verification des liens.
        self.verif = verif
        # utiliser pour l'optimisation
        self.__data = {}

    def __verif_content(self, urls, ext):
        '''
            Verification du bon format du lien
        '''
        if not self.verif:
            # si Faux pas de verification
            # reenvoie directement la liste données
            return urls
        
        new_urls = []
        for url in urls:
            # Envoie d'une requete qui recupere que l'en tête.
            try:
                rq = head(url).headers
            except Exception as err:
                print(err)
                continue
            # Verfier si le lien renvoie bien le format voulu.
            if rq.get('content-type') == f'application/{ext}':
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

    @property
    def docx(self):
        """
        Fonction pour récupérer les documents word.
      """
      #vérifier si les résultats ne sont pas déjà enregistrer
        if self.__data.get('docx'):
            if self.__data['docx'][0] == self.query:
                return self.__data['docx'][1]
        tmp = self.query
        self.query = 'filetype:docx ' + self.query
        result = self.__verif_content(self.pages, "vnd.openxmlformats-officedocument.wordprocessingml.document")
        self.query = tmp
         #  Sauvegarde des resultats pour optimiser la prochaine même appel.
        self.__data['docx'] = (self.query, result)
        return result

    @property 
    def xlsx(self):
        """Fonction pour récupérer les excels
        """
        #vérifier si les résultat ne sont pas déjà enregistrer
        if self.__data.get('xlsx'):
            if self.__data['xlsx'][0] == self.query:
                return self.__data['xlsx'][1]
        tmp = self.query
        self.query = 'filetype:xlsx ' + self.query
        result = self.__verif_content(self.pages, "vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.query = tmp
         #  Sauvegarde des resultats pour optimiser la prochaine même appel.
        self.__data['xlsx'] = (self.query, result)
        return result

    
    @property 
    def pptx(self):
        """Fonction pour récupérer les excels
        """
        #vérifier si les résultat ne sont pas déjà enregistrer
        if self.__data.get('pptx'):
            if self.__data['pptx'][0] == self.query:
                return self.__data['pptx'][1]
        tmp = self.query
        self.query = 'filetype:pptx ' + self.query
        result = self.__verif_content(self.pages, "vnd.openxmlformats-officedocument.presentationml.presentation")
        self.query = tmp
         #  Sauvegarde des resultats pour optimiser la prochaine même appel.
        self.__data['pptx'] = (self.query, result)
        return result

