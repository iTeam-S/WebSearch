from requests import get as gets
import urllib.parse
from bs4 import BeautifulSoup


def get (url, kwargs = {}):
    """
    Une fonction qui get un liens avec les différents paramètres.
    """
    headers =  {
        'User-agent' : 'Googlebot/2.1 (http://www.googlebot.com/bot.html)' 
    }  
    requete = gets(url, params = kwargs,headers = headers, timeout = 10) 

    print ('URL : "{}" , Response : [{}]'.format(requete.url,requete))  
    soup = BeautifulSoup(requete.text, 'html.parser')
    return soup 

def yahoo(search):
    """
    Une fonction qui récupère toutes les liens des images 
    resultats selon les mot-clé en paramètre.
    """
    result = []
    url = 'https://fr.images.search.yahoo.com/search/images;_ylt=AwrJS5dMFghcBh4AgWpjAQx.;_ylu=X3oDMTE0aDRlcHI2BGNvbG8DaXIyBHBvcwMxBHZ0aWQDQjY1NjlfMQRzZWMDcGl2cw--?p='+urllib.parse.quote(search)+'&fr2=piv-web&fr=yfp-t-905-s'
    soup = get(url)
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

def google(search):
    """
    Une fonction qui récupère toutes les liens des  
    resultats selon les mot-clé en paramètre.
    """
    result = []
    url = "https://www.google.com/search?client=firefox-b-d&q=" + urllib.parse.quote(search)

    soup = get(url)
    a = soup.find_all("a")

    for link in a :
        result.append(link["href"])

    return result

google("ste")