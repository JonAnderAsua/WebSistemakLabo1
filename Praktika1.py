import json

import psutil
import time
from psutil._common import bytes2human
import signal
import sys
import requests
import urllib

#apiGakoa = "KJ0S8T8BGX7C3TMN"
apiGakoa = ""

def cpu_ram(kanalId):
    while True:
        # CPU-aren ehunekoa lortu
        cpu = psutil.cpu_percent(interval=None)
        print('CPU: ' + str(cpu) + "%")

        # RAM-aren ehunekoa lortu
        ram = psutil.virtual_memory().percent
        print('RAM: '+ str(ram) + "%")

        #Datuak aplikazioara igo
        datuakIgo(ram,cpu,kanalId)
        time.sleep(15)

def handler(sig_num, frame):

    kanalaHustu(frame)

    print('\nSignal handler called with signal ' + str(sig_num))
    print('Check signal number on '
          'https://en.wikipedia.org/wiki/Signal_%28IPC%29#Default_action')
    print('\nExiting gracefully')

    sys.exit(0)

def datuakIgo(ram,cpu,kanalId): #Ram-aren eta CPU-aren datuak igo
    metodoa = 'GET'
    uria = "https://api.thingspeak.com/update.json?api_key="+str(kanalId)+"&field1="+str(cpu)+"&field2="+str(ram)
    print(uria)

    erantzuna = requests.request(metodoa, uria, allow_redirects=False)

    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason

    print(str(kodea) + "" + deskribapena)
    edukia = erantzuna.content
    print(edukia)

def kanalaDago(): #Erabiltzaileak kanala duen begiratu, kanala badu id-a hartu
    method = 'GET'
    uri = "https://api.thingspeak.com/channels.json?api_key="+apiGakoa  # Ateratzeko form-en begiratu
    erantzun = requests.request(method, uri, allow_redirects=False)
    zerrenda = json.loads(erantzun.content)
    i = 0
    kanalGakoak = [None] * len(zerrenda)
    if len(zerrenda)>0:
        print("Kanala sortuta dago")
        for j in zerrenda:
            kanalGakoak[i] = j['api_keys'] #Gako guztiak lortu
            i += 1

            for k in j['api_keys']:
                if k['write_flag']: #Kanala idazteko aukera badu if-ean sartu
                    kanalId = k['api_key']
                    cpu_ram(kanalId)
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

    if kodea == 200: #Aurreko metodora deitu kanalaren id-a lortzeko
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

     apiGakoa = str(input('Sartu apiaren gakoa mesedez...'))
     kanalId = kanalaDago()
     # SIGINT jasotzen denean, "handler" metodoa exekutatuko da
     signal.signal(signal.SIGINT, handler(kanalId))
     print('Running. Press CTRL-C to exit.')
     while True:
         pass  # Ezer ez egin