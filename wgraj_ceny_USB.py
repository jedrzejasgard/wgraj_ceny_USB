import pandas as pd
import configparser
from vendoasg.vendoasg import Vendo

config = configparser.ConfigParser()
config.read('vendo.ini')

vendoApi = Vendo(config.get('vendo','vendo_API_port'))
vendoApi.logInApi(config.get('vendo','logInApi_user'),config.get('vendo','logInApi_pass'))
vendoApi.loginUser(config.get('vendo','loginUser_user'),config.get('vendo','loginUser_pass'))

waluty = ['PLN','EUR','CHF','CZK']


with open("USB_PB_CENY_do_cennika.xls",'rb')as plik_Ani:
    data = pd.read_excel(plik_Ani,skiprows=1,usecols=['KOD','PLN','CHF','EUR','CZK'])
    print(data)
    for index, row in data.iterrows():
        for waluta in waluty:
            cena = round(row[waluta],2)
            kod = row['KOD']
            waluta_wpisywana = waluta
            print(kod,cena,waluta_wpisywana)
            if waluta == 'PLN':
                zmien_cene = vendoApi.getJson ('/json/reply/Magazyn_Towary_UstawCene', {"Token":vendoApi.USER_TOKEN,"Model":{"Towar":{"Kod":kod},"Ceny":[{"GrupaCen":{"Kod":waluta_wpisywana},"CenaNetto":cena,"Waluta":{"Kod":waluta_wpisywana}}],"DomyslnaGrupaCenID":1}})
                print(zmien_cene)
            else:
                zmien_cene = vendoApi.getJson ('/json/reply/Magazyn_Towary_UstawCene', {"Token":vendoApi.USER_TOKEN,"Model":{"Towar":{"Kod":kod},"Ceny":[{"GrupaCen":{"Kod":waluta_wpisywana},"CenaNetto":cena,"Waluta":{"Kod":waluta_wpisywana}}]}})
                print(zmien_cene)
#print(zmien_cene)