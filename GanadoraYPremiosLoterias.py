'''
Created on 06/11/2015

@author: jaleo
'''

import os
import xlwings as xw
from InfoLoteriasFromWeb import getGanadoraFromWeb, getPremiosFromWeb
from InfoLoteriasToExcel import setGanadoraToExcel, setPremiosToExcel


def GanadoraYPremiosLoterias(juego):
    #path = '/Volumes/Harddrive_HHD/Desarrollo/python/Loterias/Loterias.xlsm'
    #if os.path.isfile(path):
    #    wb = xw.Book(path)

    if juego == "PRIMITIVA":
        juegoRes = "lottoses"
        juegoPre = "lottoes"
    elif juego == "EUROMILLONES":
        juegoRes = "euromillonariases"
        juegoPre = "euromillonariaes"
    else:
        juegoRes = "quinises"
        juegoPre = "quinies"

    print ("passa por 1")

    jornadaId, jornadaDate, numeros = getGanadoraFromWeb(juego=juegoRes, year="2020")
    
    setGanadoraToExcel(jornadaId, jornadaDate, numeros)

    premios = getPremiosFromWeb(juego=juegoPre, jornadaId=jornadaId)
    
    setPremiosToExcel(premios)

if __name__ == "__main__":
    GanadoraYPremiosLoterias("EUROMILLONES")
    
