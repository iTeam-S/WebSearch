from requests import get as gets
from requests import head

def get (url, kwargs = {}):
    """
    Une fonction qui get un liens avec les différents paramètres.
    """
    headers =  {
        'User-Agent' : 'Googlebot/2.1 (http://www.googlebot.com/bot.html)' 
        }  
    requete = gets(url, params = kwargs,headers = headers, timeout = 10) 
    return requete 