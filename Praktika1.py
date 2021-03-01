import json

import psutil
import time
from psutil._common import bytes2human
import signal
import sys
import requests
import urllib

apiGakoa = "KJ0S8T8BGX7C3TMN"

def cpu_ram(kanalId):
    while True:
    # KODEA: psutil liburutegia erabiliz, %CPU eta %RAM atera
        cpu = psutil.cpu_percent(interval=None)

        value = bytes2human(cpu)
        print('CPU: ' + value)

        ram = psutil.virtual_memory()
        ram = ram.active
        ram= bytes2human(ram)
        print('RAM: '+ ram)
        datuakIgo(ram,cpu,kanalId)
        time.sleep(15)

def handler(sig_num, frame):

    kanalaHustu(frame)

    print('\nSignal handler called with signal ' + str(sig_num))
    print('Check signal number on '
          'https://en.wikipedia.org/wiki/Signal_%28IPC%29#Default_action')
    print('\nExiting gracefully')

    sys.exit(0)

def datuakIgo(ram,cpu,kanalId): #Ram eta CPU-aren datuak igotzen dira
    metodoa = 'GET'
    uria = "https://api.thingspeak.com/update.json"
    goiburuak = {'Host':'api.thingspeak.com'}
    edukia = {'apy_key':kanalId,'fieldCpu':cpu,'fieldRam':ram}

    erantzuna = requests.request(metodoa, uria,data = edukia,headers = goiburuak, allow_redirects=False)

    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason

    print(str(kodea) + "" + deskribapena)
    edukia = erantzuna.content
    print(edukia)

def kanalaDago(): #Erabiltzaileak kanala duen begiratu, kanala badu id-a hartu
    method = 'GET'
    uri = "https://api.thingspeak.com/channels.json?api_key="+apiGakoa  # Ateratzeko form-en begiratu
    erantzun = requests.request(method, uri, allow_redirects=False)
    print(uri)
    zerrenda = json.loads(erantzun.content)
    if len(zerrenda)>0:
        kanalId = zerrenda[1]['id']
        cpu_ram(kanalId)
        return kanalId
    else:
        print("Ez dago kanalik, bat sortuko da")
        kanalaSortu()

def kanalaSortu(): #Kanal berri bat sortu
    # Eskaera definitu
    metodoa = 'POST'
    uria = "https://api.thingspeak.com/channels.json"  # Ateratzeko form-en begiratu
    goiburuak = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}

    datuak = {'api_key': apiGakoa,'field1':'fieldCPU','field2':'fieldRam'}
    edukia = urllib.parse.urlencode(datuak)
    goiburuak['Content-Length'] = str(len(edukia))

    erantzuna = requests.request(metodoa, uria, data=edukia, headers=goiburuak, allow_redirects=False)

    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason

    if kodea == 200:
        kanalaDago()


def kanalaHustu(kanalId): #Dagoeneko kanala hustu
    metodoa = 'DELETE'
    uria = "https://api.thingspeak.com/channels/"+kanalId+"/feeds.json"  # Ateratzeko form-en begiratu
    goiburuak = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}

    datuak = {'api_key': apiGakoa}
    edukia = urllib.parse.urlencode(datuak)
    goiburuak['Content-Length'] = str(len(edukia))

    erantzuna = requests.request(metodoa, uria, data=edukia, headers=goiburuak, allow_redirects=False)

    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason

    print(str(kodea) + "" + deskribapena)
    print(erantzuna.content)

if __name__ == "__main__":
     kanalId = kanalaDago()
     # SIGINT jasotzen denean, "handler" metodoa exekutatuko da
     signal.signal(signal.SIGINT, handler(kanalId))
     print('Running. Press CTRL-C to exit.')
     while True:
         pass  # Ezer ez egin