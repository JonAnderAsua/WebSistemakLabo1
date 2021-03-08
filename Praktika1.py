import json
import psutil
import time
import signal
import sys
import requests
import urllib

#apiGakoa = "KJ0S8T8BGX7C3TMN"
apiGakoa = ""
kanalGakoa = ""
kanalId = ""

def cpu_ram():
    while True:
        # CPU-aren ehunekoa lortu
        cpu = psutil.cpu_percent(interval=None)
        print('CPU: ' + str(cpu) + "%")

        # RAM-aren ehunekoa lortu
        ram = psutil.virtual_memory().percent
        print('RAM: '+ str(ram) + "%")

        #Datuak aplikazioara igo
        print("Datuak igoko dira")
        datuakIgo(ram,cpu)
        time.sleep(15)

def kanalaHustu(): #Dagoeneko kanala hustu
    metodoa = 'DELETE'
    uria = "https://api.thingspeak.com/channels/" + str(kanalId) + "/feeds.json"
    print("Kanala husteko uri-a: "+uria)
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

def handler(sig_num, frame):

    print("Kanala hustuko da...")
    kanalaHustu()

    print('\nSignal handler called with signal ' + str(sig_num))
    print('\nExiting gracefully')
    print("Ctrl + C sakatu du")
    sys.exit(0)

def datuakIgo(ram,cpu): #Ram-aren eta CPU-aren datuak igo
    #Field1 = CPU-aren field-a
    #Field2 = RAM-aren field-a
    metodoa = 'GET'
    uria = "https://api.thingspeak.com/update.json?api_key=" + kanalGakoa + "&field1=" + str(cpu) + "&field2=" + str(ram)

    print("Datuak igotzeko uri-a:\n" + uria)

    erantzuna = requests.request(metodoa, uria, allow_redirects=False)

    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason

    print(str(kodea) + "" + deskribapena)
    edukia = erantzuna.content
    print(edukia)

def kanalaDago(): #Erabiltzaileak kanala duen begiratu, kanala badu eta idatzi ahal bada haren id-a hartu
    global kanalId
    method = 'GET'
    uri = "https://api.thingspeak.com/channels.json?api_key="+apiGakoa # Ateratzeko form-en begiratu
    print("Kanala sortuta dagoen ala ez ikusteko uri-a:\n"+uri)
    erantzun = requests.request(method, uri, allow_redirects=False)
    zerrenda = json.loads(erantzun.content) #Erantzunaren json-k lortu
    i = 0
    kanalGakoak = [None] * len(zerrenda)
    if len(zerrenda)>0:
        print("Kanala sortuta dago")
        for j in zerrenda:
            kanalId = j['id'] #Kanalaren id-a lortu
            print("Kanalaren id-a hurrengoa da: " + str(kanalId))
            kanalGakoak[i] = j['api_keys'] #Gako guztiak lortu
            i += 1

            for k in j['api_keys']:
                if k['write_flag']: #Kanala idazteko aukera badu if-ean sartu
                    return k['api_key']
                    cpu_ram()
    else:
        print("Ez dago kanalik, bat sortuko da")
        kanalaSortu()

def kanalaSortu(): #Kanal berri bat sortu
    # Eskaera definitu
    metodoa = 'POST'
    uria = "https://api.thingspeak.com/channels.json"  # Ateratzeko form-en begiratu
    goiburuak = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}

    datuak = {'api_key': apiGakoa}
    edukia = urllib.parse.urlencode(datuak)
    goiburuak['Content-Length'] = str(len(edukia))

    erantzuna = requests.request(metodoa, uria, data=edukia, headers=goiburuak, allow_redirects=False)

    kodea = erantzuna.status_code

    if kodea == 200: #Aurreko metodora deitu kanalaren id-a lortzeko
        kanalaDago()



if __name__ == "__main__":

     apiGakoa = str(input('Sartu apiaren gakoa mesedez...\n'))
     kanalGakoa = kanalaDago() #Kanala badago
     # SIGINT jasotzen denean, "handler" metodoa exekutatuko da
     signal.signal(signal.SIGINT, handler)
     print('Running. Press CTRL-C to exit.')
     while True:
        cpu_ram()