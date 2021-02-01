'''
Created on 06/11/2015

@author: jaleo
'''
import unicodedata
import xlwings as xw


def remover_acentos(txt):
    return ''.join((c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn'))


def setGanadoraToExcel(jornadaId, jornadaDate, fecha, numeros, wb=None):
    #if wb is None: wb = xw.Book()
    #sht = wb.sheets["working"]
    xw.Range("W3").value = jornadaId
    xw.Range("W4").value = jornadaDate
    xw.Range("F5").value = jornadaDate
    xw.Range("V20").value = fecha
    xw.Range("F6").value = numeros


def setPremiosToExcel(premios, wb=None):
    #if wb is None: wb = xw.Book()
    #sht = wb.sheets["working"]

    xw.Range("V6").value = premios
