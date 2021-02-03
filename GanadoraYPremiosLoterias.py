#!/Volumes/Harddrive_HHD/apps/python/.virtualenvs/loterias/bin/python

import os
import xlwings as xw
from InfoLoteriasFromWeb import getGanadoraFromWeb, getPremiosFromWeb
from InfoLoteriasToExcel import setGanadoraToExcel, setPremiosToExcel


def GanadoraYPremiosLoterias(juego, updXLS):
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

    jornadaId, fecha, numeros = getGanadoraFromWeb(juego=juegoRes, year="2021")
    premios = getPremiosFromWeb(juego=juegoPre, jornadaId=jornadaId)
    
    if updXLS:
        setGanadoraToExcel(juego, fecha, numeros)
        setPremiosToExcel(juego, fecha, jornadaId, premios)
    else:
        print(f"{jornadaId=}. {numeros=}")
        print(f"{premios=}")
        

####################################################################################
#  Macros excel                                                          
####################################################################################
def GanadoraYPremiosMacroExcel(juego, updXLS=True):
    # os.system('/bin/bash --rcfile /Volumes/Harddrive_HHD/Desarrollo/python/Loterias/venv.sh')
    GanadoraYPremiosLoterias(juego, updXLS)

###################################################################################
#  Test                                                                  
###################################################################################
if __name__ == "__main__":    
    GanadoraYPremiosMacroExcel("PRIMITIVA", True)
    
 