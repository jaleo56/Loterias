'''
Created on 06/11/2015

@author: jaleo
'''
import unicodedata
import xlwings as xw
from xlwings.constants import InsertShiftDirection


def remover_acentos(txt):
    return ''.join((c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn'))


def setGanadoraToExcel(juego, fecha, numeros, wb=None):
    #if wb is None: wb = xw.Book()
    #sht = wb.sheets["DASHBOARD"]
    #sht.range('A:A').insert()

    sht = xw.sheets["DASHBOARD"]
    if juego == "PRIMITIVA":
        xw.Range("M4").value = fecha
        xw.Range("H6").value  = numeros
        rango = "K3:R3"
    else:
        xw.Range("U4").value = fecha
        xw.Range("Q6").value  = numeros
        rango = "J3:P3"

    sht = xw.sheets[juego]
    my_values = sht.range('A3:DA3').options(ndim=2).value 
    sht.range("A4:DA4").insert()
    sht.range('A4:DA4').value = my_values
    sht.range("A3").value = fecha
    sht.range("B3").value  = numeros
    sht.range(rango).value  = 0


def setPremiosToExcel(juego, fecha, jornadaId, premios, wb=None):
    #if wb is None: wb = xw.Book()
    #sht = wb.sheets["DASHBOARD"]
    if juego == "PRIMITIVA":
        xw.Range("AA4").value = jornadaId
        xw.Range("Z4").value = fecha 
        xw.Range("Y6").value = premios
    else:    
        xw.Range("AA16").value = jornadaId
        xw.Range("Z16").value = fecha 
        xw.Range("Y18").value = premios