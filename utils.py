from bs4 import BeautifulSoup
from requests import get as gets

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