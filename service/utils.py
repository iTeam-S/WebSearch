from youtube_dl import YoutubeDL

def download_youtube(url ,kwargs):
    '''
    Une fonction pour télecharger les vidéos sur Youtube
        Si vous voulez seulement l'audio :
            parms :{
                'audio' : True
            }
        Si vous voulez la video :
            params : {
                'video' : True
            }
        Si vous voulz préciser le format :
            params : {
                'video' : True ,
                'format' : 160 \\160 : mp4 ,192 :  ....
            }        
    '''
    ytl_opts = {}
    if kwargs.get('audio') :
        ydl_opts = {
            'outtmpl': '../data/audio/%(title)s-%(id)s.%(ext)s', 
            'noplaylist': True,
            'continue_dl': True,
            'format': 'bestaudio/best', 
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        } 
    elif kwargs.get('video') and kwargs.get('format'):
        ydl_opts = {
            'outtmpl': '../data/video/%(title)s-%(id)s.%(ext)s',
            'noplaylist': True,
            'continue_dl': True,
            'format' : format ,
        } 
    else :
        ydl_opts = {
            'outtmpl': '../data/video/%(title)s-%(id)s.%(ext)s',
            'noplaylist': True,
            'continue_dl': True,
            'format' : 'bestvideo+bestaudio/best' ,
        } 
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.cache.remove()
            info_dict = ydl.extract_info(url, download=False)
            ydl.prepare_filename(info_dict)
            ydl.download([url])
            return ydl.prepare_filename(info_dict)
    except Exception as e:
        print(e)
        return False 
params = {
    'audio' : True ,
}
x= download_youtube('https://www.youtube.com/watch?v=BZP1rYjoBgI', params)
