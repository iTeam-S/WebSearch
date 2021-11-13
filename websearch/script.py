import urllib.parse
from bs4 import BeautifulSoup
from requests import get, head

import os
import json

__location__ = os.path.dirname(os.path.abspath(__file__))


class WebSearch:
    '''
        Module permettant de prendre les différents lien sur le web.
            * query: prend l'expression à rechercher.
            * verif: si True, lance une requete à l'url pour valider
                le bon format du résultat, pardefaut à True.
                peut être desactiver en mettant `verif=False` en argument.
            * site: pour preciser un site precis comme source
    '''
    _headers = {
        'User-Agent': 'Googlebot/2.1 (http://www.googlebot.com/bot.html)'
        }

    def __init__(self, query, verif=True, **kwargs):
        # verifier si la recherche est de type mutliple.
        if isinstance(query, list):
            self.query = "'"
            self.query += "' OR '".join(query)
            self.query += "'"
        else:
            self.query = query

        # verification du presence du site
        if kwargs.get('site'):
            self.query = f"site:{kwargs.get('site')} {self.query}"

        # Utiliser pour la verification des liens.
        self.verif = verif
        # utiliser pour l'optimisation
        self.__data = {}

    def __verif_content(self, urls, mimetype):
        '''
            Verification du bon format du lien
            argument `ext` peut être consulté ici:
            https://developer.mozilla.org/fr/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
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
            if rq.get('content-type') == mimetype:
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
        url = 'https://fr.images.search.yahoo.com/search/images;_ylt=AwrJS5dMFghcBh4AgWpjAQx.;\
        _ylu=X3oDMTE0aDRlcHI2BGNvbG8DaXIyBHBvcwMxBHZ0aWQDQjY1NjlfMQRzZWMDcGl2cw--?p='\
            + urllib.parse.quote(self.query)+'&fr2=piv-web&fr=yfp-t-905-s'

        requete = get(url, headers=self._headers, timeout=10)
        soup = BeautifulSoup(requete.text, 'html.parser')
        container = soup.find("ul", {"id": "sres"})
        try:
            lis = container.find_all('li')
        except Exception as e:
            print(e)
            return result

        if len(lis) == 0:
            return result

        for li in lis:
            try:
                img = li.find("img")
                img = str(img["data-src"]).split("&pid")
                result.append(str(img[0]))

            except Exception as e:
                print(e)
                continue

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

        url = "https://www.google.com/search?client=firefox-b-d&q="\
            + urllib.parse.quote(self.query)

        requete = get(url, headers=self._headers, timeout=10)
        soup = BeautifulSoup(requete.text, 'html.parser')
        a = soup.find_all("a")
        for link in a:
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
        result = self.__verif_content(self.pages, 'application/pdf')
        self.query = tmp
        #  Sauvegarde des resultats pour optimiser la prochaine même appel.
        self.__data['pdf'] = (self.query, result)
        return result

    @property
    def docx(self):
        """
        Fonction pour récupérer les documents word.
      """
        # vérifier si les résultats ne sont pas déjà enregistrer
        if self.__data.get('docx'):
            if self.__data['docx'][0] == self.query:
                return self.__data['docx'][1]
        tmp = self.query
        self.query = 'filetype:docx ' + self.query
        result = self.__verif_content(
            self.pages, "application/vnd.openxmlformats-officedocument"
                        ".wordprocessingml.document")

        self.query = tmp
        #  Sauvegarde des resultats pour optimiser la prochaine même appel.
        self.__data['docx'] = (self.query, result)
        return result

    @property
    def xlsx(self):
        """
            Fonction pour récupérer les excels
        """
        # vérifier si les résultat ne sont pas déjà enregistrer
        if self.__data.get('xlsx'):
            if self.__data['xlsx'][0] == self.query:
                return self.__data['xlsx'][1]
        tmp = self.query
        self.query = 'filetype:xlsx ' + self.query
        result = self.__verif_content(
            self.pages, "application/vnd.openxmlformats-officedocument"
                        ".spreadsheetml.sheet")
        self.query = tmp

        #  Sauvegarde des resultats pour optimiser la prochaine même appel.
        self.__data['xlsx'] = (self.query, result)
        return result

    @property
    def pptx(self):
        """Fonction pour récupérer les excels
        """
        # Vérifier si les résultat ne sont pas déjà enregistrer
        if self.__data.get('pptx'):
            if self.__data['pptx'][0] == self.query:
                return self.__data['pptx'][1]
        tmp = self.query
        self.query = 'filetype:pptx ' + self.query

        result = self.__verif_content(
            self.pages, "application/vnd.openxmlformats-officedocument"
                        ".presentationml.presentation")
        self.query = tmp

        # Sauvegarde des resultats pour optimiser la prochaine même appel.
        self.__data['pptx'] = (self.query, result)
        return result

    @property
    def odt(self):
        '''
            Fonction pour recuperer que les documents odt.
        '''
        # On vérifie que les résultats ne sont pas déjà enregistrés.
        if self.__data.get('odt'):
            if self.__data['odt'][0] == self.query:
                return self.__data['odt'][1]
        tmp = self.query
        self.query = 'filetype:odt ' + self.query

        result = self.__verif_content(
            self.pages, "application/vnd.oasis.opendocument.text")
        self.query = tmp

        # Sauvegarde des resultats pour optimiser la prochaine même appel.
        self.__data['odt'] = (self.query, result)
        return result

    @property
    def ods(self):
        '''
            Fonction pour recuperer que les documents ods.
        '''
        # On vérifie que les résultats ne sont pas déjà enregistrés.
        if self.__data.get('ods'):
            if self.__data['ods'][0] == self.query:
                return self.__data['ods'][1]
        tmp = self.query
        self.query = 'filetype:ods ' + self.query
        result = self.__verif_content(
            self.pages, "application/vnd.oasis.opendocument.spreadsheet")
        self.query = tmp
        # Sauvegarde des resultats pour optimiser la prochaine même appel.
        self.__data['ods'] = (self.query, result)
        return result

    @property
    def odp(self):
        '''
            Fonction pour recuperer que les documents odp.
        '''
        # On vérifie que les résultats ne sont pas déjà enregistrés.
        if self.__data.get('odp'):
            if self.__data['odp'][0] == self.query:
                return self.__data['odp'][1]
        tmp = self.query
        self.query = 'filetype:odp ' + self.query
        result = self.__verif_content(
            self.pages, "application/vnd.oasis.opendocument.presentation")
        self.query = tmp
        # Sauvegarde des resultats pour optimiser la prochaine même appel.
        self.__data['odp'] = (self.query, result)
        return result

    @property
    def kml(self):
        '''
            Fonction pour recuperer des fichiers de projets géographiques
            pour google earth sous la format kml
        '''
        # On vérifie que les résultats ne sont pas déjà enregistrés.
        if self.__data.get('kml'):
            if self.__data['kml'][0] == self.query:
                return self.__data['kml'][1]
        tmp = self.query
        self.query = 'filetype:kml ' + self.query
        result = self.__verif_content(
            self.pages, "application/vnd.google-earth.kml+xml")
        self.query = tmp

        # Sauvegarde des resultats pour optimiser la prochaine même appel.
        self.__data['kml'] = (self.query, result)
        return result

    def custom(self, extension='pdf', mimetype=None):
        '''
            Fonction pour recuperer des fichiers en fonction
            de l'extension voulu et des type de mime que ce dernier utilise

            Keyword arguments:
            extension -- The file's extension (default pdf)
            mimetype -- The mimetype that match the extension (default pdf)
        '''
        # On verifie que les resultats n'est pas deja enregistrer.
        if self.__data.get(extension):
            if self.__data[extension][0] == self.query:
                return self.__data[extension][1]
        tmp = self.query
        self.query = f'filetype:{extension} {self.query}'

        if not mimetype:
            with open(os.path.join(__location__, 'extension.json')) as file:
                mimetype = json.load(file).get(extension)

        if mimetype:
            result = self.__verif_content(self.pages, mimetype)
            self.query = tmp
            #  Sauvegarde des resultats pour optimiser la prochaine même appel.
            self.__data[extension] = (self.query, result)
            return result
        else:
            return """Can't find mimetype that match this extension\n
                Please provide the mimetypes as arguments.
            """

    def custom_search(self, *args, **kwargs):
        raise Exception(
            "`custom_search` is deprecated since v1.0.4, use `custom` instead")
