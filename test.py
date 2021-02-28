def potencia(c):
    """Calcula y devuelve el conjunto potencia del 
       conjunto c.
    """
    if len(c) == 0:
        return [[]]

    print(f'Antes: {c=}')    
    r = potencia(c[:-1])
    print(f'Despues: {r=}')
    return r + [s + [c[-1]] for s in r]

# potencia(['1', '2', '3'])

def combi():
    n, fin = 0, 49+1
    for a in range(1, fin):
        for b in range(a+1, fin):
                l = [a, b]
                print (n:=n+1, l)

combi()

    #return [s for s in potencia(c) if len(s) == n]
    # combinaciones(['0', '1', '2', '3', '4', '5', '6', '7'], 6))



def iteracion():
    i = 0

    while True:
        i += 1
        entrada = input('Quieres continuar ?:')
        if entrada in ("no", "n"):
            break
        else:
            print(f"otra iteracion {i}")

# iteracion()

# import pandas as pd

# students_grades = pd.read_excel('./Libro2.xlsx')
# students_grades.head()
# print(f'{students_grades=}')

# if __name__ == "__main__":
#     combi()

# def check():
#     l = [1, 2, 3, 7, 8, 9]
#     seguidos = [0] * 7
#     seg = 0
#     for i in range(1, 6):
#         if l[i] - l[i-1] == 1:
#             seg += 1
#         else:
#             if seg > 0: seguidos[seg] += 1
#             seg = 0
#     else:
#         if seg > 0: seguidos[seg] += 1

#     print (f"{seguidos=}")

# def rango():
#     for i in range(1,10):
#         print (f"{i=}")

# def seguidos():
#     numant=5
#     terminacion = numant % 10
#     nFiguras=[[2, 6, 8, 10, 20], [12, 14, 16, 18, 22], [40, 46, 48], [34, 38, 26]]
#     for i in range(len(nFiguras)):
#         nFiguras[i] = [x for x in nFiguras[i] if int(x) != numant+1]
#         nFiguras[i] = [x for x in nFiguras[i] if int(x) % 10 != terminacion]
#     print (f"{numant=}. {nFiguras=}")


# def _checkSeguidos(lCombinacion):
#         lSeguidos = [0] * 7
#         seg = 0
#         for i in range(1, 6):
#             if lCombinacion[i] - lCombinacion[i-1] == 1:
#                 seg += 1
#             else:
#                 if seg > 0: lSeguidos[seg] += 1
#                 seg = 0
#         else:
#             if seg > 0: lSeguidos[seg] += 1 

#         for i in range(6): 
#             if lSeguidos[i] > 0: lSeguidos[6] += 1  
        
#         return lSeguidos

# # from datetime import datetime
# # import locale

# # locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))

# from utils import getFecha

# def fecha():
#     jornadaDate='sa,\xa030\xa0ene\xa02021'
#     print(getFecha(jornadaDate))

#     # jornadaDate = jornadaDate[:2] + jornadaDate[2:]    
#     # jornadaDate = _publicarData(jornadaDate[4:])
#     # print(f"{jornadaDate=}")

#     # Convertimos un string con formato
#     # <día> del <mes> de <año> a las <hora>:<minutos> en datetime
#     # una_fecha = '20 del 04 de 2019 a las 12:00'
#     # fecha_dt = datetime.strptime(jornadaDate, '%d %b %Y')
#     # print(fecha_dt.date().strftime('%d/%m/%Y'))


#     # from datetime import datetime
#     # import locale

#     # locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))

#     # jornadaDate = jornadaDate[4:]
#     # jornadaDate = jornadaDate.replace('\xa0', ' ')
#     # fecha_dt = datetime.strptime(jornadaDate, '%d %b %Y')
#     # fecha = fecha_dt.date().strftime('%d/%m/%Y')


# # def _publicarData(txt):
# #     txt = txt.replace('\xa0', ' ')
# #     # txt.encode('utf-8')
# #     #txt = re.sub('\xa0', ''.encode('utf-8'), txt)
# #     return txt

# def sw(sheet, loto):
#     apuestas_cell = {
#         "DASHBOARD_EUROMILLONES"    : "Q10",
#         "DASHBOARD_PRIMITIVA"       : "H10",
#         "PRIMITIVA_PRIMITIVA"       : "K3",
#         "EUROMILLONES_EUROMILLONES" : "K3" 
#     }
#     print(apuestas_cell.get(sheet + "_" + loto, "E001: Invalid sheet or loto"))


# while not found:
#             apuesta = [0] * s.NUMS_COMBINACION
#             n = 0
#             for i in range(s.NUMS_COMBINACION ):
#                 # # ---- NUMEROS DE N GRUPOS: BIP, BIC, BPP, BPC, AIP, AIC, APP, APC
#                 # n = self.bombo.getNumeroFiguras(s, idx=i, numant=0, ndecenas=0, ngrupos=8)
#                 # apuesta[i] = n 


#                 # ---- NUMEROS AL AZAR
#                 # apuesta[i] = self.bombo.getNumeroAlAzar(s, repetir=False)

#                 # ---- NUMEROS TERMINACIONES DIFERENTES
#                 apuesta[i] = self.bombo.getNumeroTerminacion(s, idx=i, terminacion=t)
#                 t = apuesta[i] % 10

#                 # ---- ALTERAR NUMEROS
#                 # if i == 0:
#                 #     apuesta[i] = self.bombo.getNumeroAlAzar()
#                 #
#                 # ---- ...(1) ALTOS Y BAJOS
#                 # elif ultimo < 26:                            
#                 #     apuesta[i] = self.bombo.getNumeroAlto()
#                 # else:
#                 #     apuesta[i] = self.bombo.getNumeroBajo()
#                 #
#                 # ---- ...(2) PERIFERIA Y CENTRALES
#                 # elif: ultimo in self.bombo.numerosInitPeriferia:
#                 #   apuesta[i] = self.bombo.getNumeroBajo()
#                 #
#                 # ultimo = apuesta[i]
            
#             # Control de decenas
#             lDecenas = [0] * 6
#             fDecenas = ""
#             for n in apuesta:
#                 d = int(n/10)
#                 lDecenas[d] += 1

#             lDecenas.sort(reverse=True)
#             for n in lDecenas:
#                 if n > 0: 
#                     fDecenas += str(n) if fDecenas == "" else str("|") + str(n)
            
#             # if fDecenas in ("3|2|1", "2|2|1|1", "3|1|1|1"):
#             if fDecenas in ("2|2|1|1"):
#                 if len(apuesta) == len(set(apuesta)): 
#                     found = True
#                 else: apuestas_erroneas += 1
#             else: apuestas_erroneas += 1




# if __name__ == "__main__":
#     # s = _checkSeguidos([16, 20, 31, 32, 35, 48])
#     # print(s)
#     # fecha()
#     sw("PRIMITIVA", "PRIMITIVAS")




#     # def _checkNAnteriores(self, s, fuera=True, nAnteriores=7):
#     #     nApuestas = []
#     #     lAciertos = []
#     #     for i in range(len(self.ganadoras)-nAnteriores):
#     #         sGanadora = set(self.ganadoras.iloc[i])
#     #         nApuestas.clear()    
#     #         for j in range(1,nAnteriores+1):
#     #             l = self.ganadoras.iloc[i+j].tolist()
#     #             nApuestas += l
#     #
#     #         if fuera:
#     #            cApuestas = [x for x in self.s.NUMEROS_LOTO if x not in nApuestas]
#     #         sApuestas = set(cApuestas)
#     #
#     #         nAciertos = len(sGanadora.intersection(sApuestas))
#     #         l2 = [nAciertos, len(sApuestas)]
#     #         lAciertos.append(l2)
#     #     return lAciertos 
    

#     # Get numeros y estrellas APUESTAS de las 10 ganadoras anteriores    
#     # def _getApuestas(self, nganadora=None):
#     #     if nganadora == None:
#     #         return self.apuestas, self.eApuestas
#     #     else:
#     #         apuestas  = []
#     #         estrellas = []
#     #         for y in range(nganadora+1, nganadora+11):
#     #             apuestas.append(self.ganadoras.iloc[y])
#     #             estrellas.append(self.eGanadoras.iloc[y])
#     #         dfApuestas = pd.DataFrame(apuestas)
#     #         dfEstrellas = pd.DataFrame(estrellas)
#     #         return dfApuestas, dfEstrellas

