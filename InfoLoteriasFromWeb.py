#!/Volumes/Harddrive_HHD/apps/python/.virtualenvs/loterias/bin/python

import re
import requests
from bs4 import BeautifulSoup
import unicodedata
from utils import getFecha


def getGanadoraFromWeb(juego, year):
    url = 'http://www.elgordo.com/results/' + juego + '.asp?y=' + year
    numeros = []

    page_response = requests.get(url, timeout=5)
    soup = BeautifulSoup(page_response.content, "html.parser")

    if juego == "lottoses":
        lit1 = soup.find("table", {"class": "tbl no-responsive tp"})
    else:
        lit1 = soup.find("table", {"class": "tbl no-responsive ee"})
    lit2 = lit1.find("tbody")

    jornadaDate = lit2.findAll("a")[0].getText()
    jornadaDate = jornadaDate[:2] + jornadaDate[2:]
    jornadaDate = _publicarData(jornadaDate)
    fecha = getFecha(jornadaDate)

    jornadaId = lit2.findAll('a')[0].get('href')
    jornadaId = jornadaId[-5:]
    jornadaId = _publicarData(jornadaId)

    fin = 6 if juego == "lottoses" else 5

    for i in range(0, fin):
        res = lit2.findAll("td", {"class": "d hide-responsive"})[i].getText()
        numeros.append(res)

    # if fin == 5: numeros.append(0)

    for i in range(0, 2):
        res = lit2.findAll("td", {"class": "d ex hide-responsive"})[i].getText()
        numeros.append(res)

    return jornadaId, fecha, numeros


def getPremiosFromWeb(juego, jornadaId):

    url ='http://www.elgordo.com/results/' + juego + '.asp?sort=' + jornadaId
    page_response = requests.get(url, timeout=5)
    soup = BeautifulSoup(page_response.content, "html.parser")

    if juego == "lottoes":
        fin = 6
        all_rows  = soup.find("table", { "class" : "tbl no-responsive tp size80 tbl-result" })
    else:
        fin = 13
        all_rows  = soup.find("table", { "class" : "tbl no-responsive ee size80 tbl-result" })
    premios = list()
    cat = [0] * fin
    for i in range(0, fin):
        cat = all_rows.findAll("td", {"data-title": "Cat:"})[i].getText()
        ace = all_rows.findAll("td", {"data-title": "Acertantes:"})[i].getText()
        pre = all_rows.findAll("td", {"data-title": "Premios:"})[i].getText()
        pre = re.sub('\xa0', ' ', pre)
        pre = re.sub('\u20ac', 'E', pre)
        t = (cat, ace, pre)
        premios.append(t)
    return premios


def _remover_acentos(txt):
    return ''.join((c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn'))


def _publicarData(txt):
    txt.encode('utf-8')
    #txt = re.sub('\xa0', ''.encode('utf-8'), txt)
    return txt