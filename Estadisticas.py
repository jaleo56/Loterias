import pandas as pd
from HojaExcel import HojaExcel
from settings import Settings

class Estadisticas:
    lAciertos = []
    lResumen = []
    resultadosRange = []

    def __init__(self, file, sheet):
        self.s = Settings(file, sheet)

    ########################################################################################
    # API
    #---------------------------------------------------------------------------------------
    def checkAciertos(self, updXLS=False):
        xls = self._getInfoFromExcel()      # Obtiene, apuestas, eApuestas, ganadoras,
        snApuestas = self._getNumsApuestas(self.apuestas)
        self.lAciertos = self._checkAciertos(self.ganadoras, snApuestas)
        if updXLS:
            xls.publicarRango(self.s.CEL_ACIERTOS, self.lAciertos)
        else:
            print (f"{self.lAciertos=}")


    def checkNAnteriores(self, updXLS=None, nAnteriores=10):
        xls = self._getGanadorasFromExcel()     
        self.lAciertos = self._checkNAnteriores(nAnteriores)
        if updXLS != None:
           xls.publicarRango(self.s.CEL_ACIERTOS, self.lAciertos)


    def checkAllGanadoras(self, updXLS=False, resumir=False):
        xls = self._getInfoFromExcel()
        self.lAciertos, self.lResumen = self._checkGanadoras()
        if updXLS:
            resumen = [self.lResumen]
            for l in self.resultadosRange:
                resumen.append(l)
            if resumir:
                xls.publicarRango(self.s.CEL_RESUMEN, resumen)
            else:
                xls.publicarRango(self.s.CEL_RESULTADOS,  self.lAciertos)


    def checkFiguras(self, updXLS=None):
        xls = self._getGanadorasFromExcel()
        self.lFiguras = self._checkFiguras()
        if updXLS != None:
            xls.publicarRango(self.s.COL_FIGURAS, self.lFiguras)


    def checkDistribucion(self, updXLS=None):
        xls = self._getGanadorasFromExcel()
        self.lDistribucion = self._checkDistribucion()
        if updXLS != None:
            xls.publicarRango(self.s.COL_DISTRIBUCION, self.lDistribucion)        
 

    def checkSeguidos(self, updXLS=None):
        xls = self._getGanadorasFromExcel()
        self.lSeguidos = self._checkSeguidos()
        if updXLS != None:
            xls.publicarRango(self.s.COL_SEGUIDOS, self.lSeguidos)   
        else:
            print(self.lSeguidos)
            
  
    ########################################################################################
    # MODULOS INTERNOS. NIVEL 1
    #---------------------------------------------------------------------------------------
    def _checkAciertos(self, ganadoras, nssApuestas):
        lAciertos =[]
        nNumeros = len(nssApuestas)
        for x, ganadora in ganadoras.iterrows():
            if x == 0: continue
            sGanadora = set(ganadora)
            naciertos = len(sGanadora.intersection(nssApuestas))
            lFila = [naciertos, nNumeros]
            lAciertos.append(lFila)
        return lAciertos


    def _checkGanadoras(self):
        lAciertos =[]
        resumen = []
        for x in range(len(self.ganadoras)):
            neRow = []
            cntRow = [0] * 61
            snGanadora = set(self.ganadoras.iloc[x])
            seGanadora = set(self.eGanadoras.iloc[x])
            # apuestas, estrellas = self._getApuestas(nganadora=x)
            for y in range(len(self.apuestas)):
                snApuesta = set(self.apuestas.iloc[y])
                seApuesta = set(self.eApuestas.iloc[y])
                nums = len(snGanadora.intersection(snApuesta))
                if self.s.LOTO == "PRIMITIVA":
                    ests = len(seGanadora.intersection(snApuesta))
                else:
                    ests = len(seGanadora.intersection(seApuesta))
                neRow.append(nums)
                neRow.append(ests)
                cntRow[(nums*10)+ests] += 1
            for z in range(len(self.apuestas), 10):
                neRow.append("")
                neRow.append("")
            res = self._listaAciertos(cntRow)
            lAciertos.append(neRow + res)
            resumen.append(res)

        total = pd.DataFrame(resumen).sum()
        lTotal = total.tolist()
        return lAciertos, lTotal


    def _checkFiguras(self):
        lFiguras = []
        self._inicioArraysNumeros()
        for i, ganadora in self.ganadoras.iterrows():
            sGanadora   = set(ganadora)
            pares       = len(sGanadora.intersection(self.numerosPares))
            impares     = self.s.NUMS_COMBINACION - pares
            bajos       = len(sGanadora.intersection(self.numerosBajos))
            altos       = self.s.NUMS_COMBINACION - bajos
            periferia   = len(sGanadora.intersection(self.numerosPeriferia))
            centrales   = self.s.NUMS_COMBINACION - periferia

            lTerminaciones  = [0] * 11
            lDecenas        = [0] * 7
            lIntervalos     = [0] * 11
            for n in ganadora:
                t = int(n%10)
                d = int(n/10)
                v = int(n/5) if n%5 != 0 else int(n/5)-1
                lTerminaciones[t] += 1
                lDecenas[d]       += 1
                lIntervalos[v]    += 1 

            for n in range(10):
                if lTerminaciones[n] > 0: lTerminaciones[10] += 1

            for n in range(6):
                if lDecenas[n] > 0: lDecenas[6] += 1

            for n in range(10):
                if lIntervalos[n] > 0: lIntervalos[10] += 1

            l = [altos, bajos, pares, impares, periferia, centrales]
            l.extend(lTerminaciones)
            l.extend(lIntervalos)
            # l.extend(lDecenas)

            lFiguras.append(l)    
        return lFiguras


    def _checkDistribucion(self):
        lDistribucion = []
        for i in range(len(self.ganadoras)):
            sGanadora = set(self.ganadoras.iloc[i])
            ac = [0] * 9
            for x in range(len(self.s.GRUPOS_NUMS)):
                numeros = set(self.s.GRUPOS_NUMS[x])
                ac[x] = len(sGanadora.intersection(numeros))  
            nGrupos = 0
            for na in ac:
                if na > 0: nGrupos += 1    
            ac[8] = nGrupos      
            lDistribucion.append(ac)    
        return lDistribucion


    def _checkNAnteriores(self, nAnteriores=7):
        nApuestas = []
        lAciertos = []
        for i in range(len(self.ganadoras)-nAnteriores):
            sGanadora = set(self.ganadoras.iloc[i])
            nApuestas.clear()    
            for j in range(1,nAnteriores+1):
                l = self.ganadoras.iloc[i+j].tolist()
                nApuestas += l
            cApuestas = [x for x in self.s.NUMEROS_LOTO if x not in nApuestas]
            sApuestas = set(cApuestas)
            nAciertos = len(sGanadora.intersection(sApuestas))
            l2 = [nAciertos, len(sApuestas)]
            lAciertos.append(l2)
        return lAciertos


    def _checkSeguidos(self):
        lSeguidos = []
        for x, ganadora in self.ganadoras.iterrows():
            if x == 0: continue
            lGanadora = list(ganadora)
            seguidos = [0] * 7
            seg = 0
            for i in range(1, 6):
                if lGanadora[i] - lGanadora[i-1] == 1:
                    seg += 1
                else:
                    if seg > 0: seguidos[seg] += 1
                    seg = 0
            else:
                if seg > 0: seguidos[seg] += 1 
            for i in range(6): 
                if seguidos[i] > 0: seguidos[6] += 1  
            lSeguidos.append(seguidos)    
        return lSeguidos

    ########################################################################################
    # MODULOS INTERNOS. NIVEL 2
    #---------------------------------------------------------------------------------------
    def _inicioArraysNumeros(self):
        self.numerosPares = [x for x in range(1, self.s.NUM_MAYOR + 1) if x % 2 == 0]
        self.numerosBajos = [x for x in range(1, 26)]
        self.numerosPeriferia = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 20, 21, 30, 31, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]

    
    def _getInfoFromExcel(self):
        xls = HojaExcel()
        ganadorasRange = xls.getDataFrame(self.s.FILE_NAME, self.s.SHEET, self.s.RNG_GANADORAS)  
        self.ganadoras = pd.DataFrame(ganadorasRange, columns=self.s.COLS_GANADORAS)
        self.eGanadoras = pd.DataFrame(ganadorasRange, columns=self.s.COLS_EGANADORAS )

        apuestasRange = xls.getDataFrame(self.s.FILE_NAME, self.s.SHEET, self.s.RNG_APUESTAS)
        self.apuestas = pd.DataFrame(apuestasRange, columns=self.s.COLS_APUESTAS)
        self.eApuestas = pd.DataFrame(apuestasRange, columns=self.s.COLS_EAPUESTAS)

        self.resultadosRange = xls.getRange(self.s.FILE_NAME, self.s.SHEET, self.s.RNG_RESUMENES)
        return xls

    
    def _getGanadorasFromExcel(self):
        xls = HojaExcel()
        ganadorasRange = xls.getDataFrame(self.s.FILE_NAME, self.s.SHEET, self.s.RNG_GANADORAS) 
        self.ganadoras = pd.DataFrame(ganadorasRange, columns=self.s.COLS_GANADORAS)
        return xls

        
    def _getApuestas(self, nganadora=None):
        if nganadora == None:
            return self.apuestas, self.eApuestas
        else:
            apuestas = []
            estrellas = []
            for y in range(nganadora+1, nganadora+11):
                apuestas.append(self.ganadoras.iloc[y])
                estrellas.append(self.eGanadoras.iloc[y])
            dfApuestas = pd.DataFrame(apuestas)
            dfEstrellas = pd.DataFrame(estrellas)
            return dfApuestas, dfEstrellas


    def _getNumsApuestas(self, apuestas):
        nApuestas =[]
        for y, apuesta in apuestas.iterrows():
            if y == 0: continue
            l = [*apuesta]
            nApuestas = nApuestas + l
        return set(nApuestas)


    def _listaAciertos(self, cntRow):
        if self.s.LOTO == "PRIMITIVA":
            return ([
                cntRow[30] + cntRow[31], cntRow[40], cntRow[41],
                cntRow[50], cntRow[51], cntRow[60]
            ])
        else:
            return ([
                cntRow[2], cntRow[12], 
                cntRow[20], cntRow[21], cntRow[22],
                cntRow[30], cntRow[31], cntRow[32],
                cntRow[40], cntRow[41], cntRow[42],
                cntRow[50], cntRow[51], cntRow[52],
                cntRow[60]
            ])


########################################################################################
# MACROS EXCEL
#---------------------------------------------------------------------------------------
def AciertosMacroExcel(file, sheet):
    std = Estadisticas(file, sheet)
    std.checkAciertos(updXLS=True)

def CheckGanadorasMacroExcel(file, sheet):
    std = Estadisticas(file, sheet)
    std.checkAllGanadoras(updXLS=True, resumir=True)

def CheckFigurasMacroExcel(file, sheet):
    std = Estadisticas(file, sheet)
    std.checkFiguras(updXLS="yes")

def CheckDistribucionMacroExcel(file, sheet):
    std = Estadisticas(file, sheet)
    std.checkDistribucion(updXLS="yes")

def CheckNAnterioresMacroExcel(file, sheet):
    std = Estadisticas(file, sheet)
    std.checkNAnteriores(updXLS="yes", nAnteriores=7)
def CheckSeguidosMacroExcel(file, sheet):
    std = Estadisticas(file, sheet)
    std.checkSeguidos(updXLS="yes")

########################################################################################
# TEST LOCAL
#---------------------------------------------------------------------------------------
if __name__ == "__main__":
    # CheckNAnterioresMacroExcel    ("Loterias3.xlsm", "PRIMITIVA")
    # CheckDistribucionMacroExcel   ("Loterias3.xls", "PRIMITIVA")
    CheckGanadorasMacroExcel        ("Test.xlsx", "PRIMITIVA")
    # CheckFigurasMacroExcel        ("Loterias3.xlsm", "PRIMITIVA")
    # CheckSeguidosMacroExcel       ("Loterias3.xlsm", "PRIMITIVA")
    # AciertosMacroExcel            ("Test.xlsx", "PRIMITIVA")
