'''
Created on 06/11/2015

@author: jaleo
'''
import unicodedata
import xlwings as xw


def remover_acentos(txt):
    return ''.join((c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn'))


def setGanadoraToExcel(juego, fecha, numeros, wb=None):
    #if wb is None: wb = xw.Book()
    #sht = wb.sheets["working"]
    if juego == "PRIMITIVA":
        xw.Range("M4").value = fecha
        xw.Range("H6").value  = numeros
    else:
        xw.Range("U4").value = fecha
        xw.Range("Q6").value  = numeros


def setPremiosToExcel(juego, fecha, jornadaId, premios, wb=None):
    #if wb is None: wb = xw.Book()
    #sht = wb.sheets["working"]
    if juego == "PRIMITIVA":
        xw.Range("AA4").value = jornadaId
        xw.Range("Z4").value = fecha 
        xw.Range("Y6").value = premios
    else:    
        xw.Range("AA16").value = jornadaId
        xw.Range("Z16").value = fecha 
        xw.Range("Y18").value = premios