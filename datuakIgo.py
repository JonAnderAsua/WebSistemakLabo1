import requests
import urllib

#Eskaerak 4 atal ditu: metodoa,uria,goiburuak eta edukia

#Eskaera definitu
metodoa = 'GET'
uria = "https://api.thingspeak.com/update?api_key=KJ0S8T8BGX7C3TMN&field1=123&field2=123"  #Ateratzeko form-en begiratu
print(uria)
goiburuak = {'Host':'api.thingspeak.com',
             'Content-Type':'application/x-www-form-urlencoded'}

erantzuna = requests.request(metodoa,uria,allow_redirects = False)

kodea = erantzuna.status_code
deskribapena = erantzuna.reason

print(str(kodea)+""+deskribapena)
edukia = erantzuna.content
print(edukia)
