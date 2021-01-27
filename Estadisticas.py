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

    def checkFiguras(self, updXLS=None):
        xls = self._getInfoFromExcel(tipo="APUESTAS")
        self.lFiguras = self._checkFiguras(self.apuestas)
        if updXLS != None:
            xls.publicarRango(self.s.COL_FIGURAS, self.lFiguras)

     
    def checkSeguidos(self, updXLS=None):
        xls = self._getInfoFromExcel(tipo="APUESTAS")
        self.lSeguidos = self._checkSeguidos(self.apuestas)
        if updXLS != None:
            xls.publicarRango(self.s.COL_SEGUIDOS, self.lSeguidos)   
        else:
            print(self.lSeguidos)
            
    
    def checkDistribucion(self, updXLS=True):
        xls = self._getInfoFromExcel(tipo="APUESTAS")
        self.lDistribucion = self._checkDistribucion(self.apuestas)
        if updXLS:
            xls.publicarRango(self.s.COL_DISTRIBUCION, self.lDistribucion)   
  
    ########################################################################################
    # MODULOS INTERNOS. NIVEL 1
    #---------------------------------------------------------------------------------------
    
    def _checkEstadisticas(self, dfCombis):
        lEstadisticas = []
        lRes = [] 
        for i, combi in dfCombis.iterrows():
            sCombi = set(combi)
            lf = self._figuras(sCombi)
            ls = self._seguidos(sCombi)
            ld = self._distribucion(sCombi)
            lRes = lf
            lRes.extend(ls)
            lRes.extend(ld)
            lEstadisticas.append(lRes)    
        return lEstadisticas


    def _checkFiguras(self, dfCombinaciones):
        lFiguras = []
        self._inicioArraysNumeros()
        for i, combinacion in dfCombinaciones.iterrows():
            sCombinacion= set(combinacion)
            pares       = len(sCombinacion.intersection(self.numerosPares))
            impares     = self.s.NUMS_COMBINACION - pares
            bajos       = len(sCombinacion.intersection(self.numerosBajos))
            altos       = self.s.NUMS_COMBINACION - bajos
            periferia   = len(sCombinacion.intersection(self.numerosPeriferia))
            centrales   = self.s.NUMS_COMBINACION - periferia

            lTerminaciones  = [0] * 11
            lDecenas        = [0] * 7
            lIntervalos     = [0] * 11
            for n in sCombinacion:
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


    def _checkSeguidos(self, dfCombinaciones):
        lSeguidos = []
        for x, combinacion in dfCombinaciones.iterrows():
            if x == 0: continue
            lCombinacion = list(combinacion)
            seguidos = [0] * 7
            seg = 0
            for i in range(1, 6):
                if lCombinacion[i] - lCombinacion[i-1] == 1:
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

    
    def _checkDistribucion(self, dfCombinaciones):
        lDistribucion = []
        for i in range(len(dfCombinaciones)):
            sCombinacion = set(dfCombinaciones.iloc[i])
            ac = [0] * 9
            for x in range(len(self.s.GRUPOS_NUMS)):
                numeros = set(self.s.GRUPOS_NUMS[x])
                ac[x] = len(sCombinacion.intersection(numeros))  
            nGrupos = 0
            for na in ac:
                if na > 0: nGrupos += 1    
            ac[8] = nGrupos      
            lDistribucion.append(ac)    
        return lDistribucion


    ########################################################################################
    # MODULOS INTERNOS. NIVEL 2
    #---------------------------------------------------------------------------------------
    def _inicioArraysNumeros(self):
        self.numerosPares = [x for x in range(1, self.s.NUM_MAYOR + 1) if x % 2 == 0]
        self.numerosBajos = [x for x in range(1, 26)]
        self.numerosPeriferia = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 20, 21, 30, 31, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]

    
    def _getInfoFromExcel(self, tipo="GANADORAS"):
        xls = HojaExcel()

        if tipo not in ("GANADORAS", "APUESTAS", "ALL"):
            raise Exception(f"Valor del parametro TIPO es erróneo. {tipo=}")

        if tipo in ("GANADORAS", "ALL"):
            ganadorasRange = xls.getDataFrame(self.s.FILE_NAME, self.s.SHEET, self.s.RNG_GANADORAS)  
            self.ganadoras = pd.DataFrame(ganadorasRange, columns=self.s.COLS_GANADORAS)
            self.eGanadoras = pd.DataFrame(ganadorasRange, columns=self.s.COLS_EGANADORAS )

        if tipo in ("APUESTAS", "ALL"):
            apuestasRange = xls.getDataFrame(self.s.FILE_NAME, self.s.SHEET, self.s.RNG_APUESTAS)
            self.apuestas = pd.DataFrame(apuestasRange, columns=self.s.COLS_APUESTAS)
            self.eApuestas = pd.DataFrame(apuestasRange, columns=self.s.COLS_EAPUESTAS)

        if tipo in ("ALL"):
            self.resultadosRange = xls.getRange(self.s.FILE_NAME, self.s.SHEET, self.s.RNG_RESUMENES)
        
        return xls


    def _getNumsApuestas(self, apuestas):
        nApuestas =[]
        for y, apuesta in apuestas.iterrows():
            if y == 0: continue
            l = [*apuesta]
            nApuestas = nApuestas + l
        return set(nApuestas)

########################################################################################
# MACROS EXCEL
#---------------------------------------------------------------------------------------

def CheckFigurasMacroExcel(file, sheet):
    std = Estadisticas(file, sheet)
    std.checkFiguras(updXLS=True)

def CheckDistribucionMacroExcel(file, sheet):
    std = Estadisticas(file, sheet)
    std.checkDistribucion(updXLS=True)

def CheckSeguidosMacroExcel(file, sheet):
    std = Estadisticas(file, sheet)
    std.checkSeguidos(updXLS=True)

########################################################################################
# TEST LOCAL
#---------------------------------------------------------------------------------------
if __name__ == "__main__":
    # CheckFigurasMacroExcel        ("Test.xlsm", "PRIMITIVA")
    # CheckSeguidosMacroExcel       ("Test.xlsm", "PRIMITIVA")
    CheckDistribucionMacroExcel   ("Test.xlsm", "PRIMITIVA")
