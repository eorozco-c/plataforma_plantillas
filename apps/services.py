import requests,datetime

def get_festivos():
    now = datetime.datetime.now()
    url = f'https://apis.digital.gob.cl/fl/feriados/{now.year}' 
    headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    params = {}
    r = requests.get(url,headers=headers, params=params)
    festivos = r.json()
    return festivos