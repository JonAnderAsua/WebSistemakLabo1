import requests
import urllib

#Eskaerak 4 atal ditu: metodoa,uria,goiburuak eta edukia

def kanalaDago():
    method = 'GET'
    uri = "https://api.thingspeak.com/update?api_key=KJ0S8T8BGX7C3TMN"  # Ateratzeko form-en begiratu
    erantzun = requests.request(method, uri, allow_redirects=False)
    kode = erantzun.status_code
    lista = erantzun.content
    if kode == 200:
        listaDago = True

    if


deskribapena = erantzuna.reason
lista = json.loads(erantzuna.content)

#Eskaera definitu
metodoa = 'POST'
uria = "https://api.thingspeak.com/channels.json" #Ateratzeko form-en begiratu
goiburuak = {'Host':'api.thingspeak.com',
             'Content-Type':'application/x-www-form-urlencoded'}

datuak = {'api_key':'KJ0S8T8BGX7C3TMN'}
edukia = urllib.parse.urlencode(datuak)
goiburuak['Content-Length'] = str(len(edukia))

erantzuna = requests.request(metodoa,uria,data = edukia,headers = goiburuak,allow_redirects = False)

kodea = erantzuna.status_code
deskribapena = erantzuna.reason

print(str(kodea)+""+deskribapena)
edukia = erantzuna.content
print(edukia)
