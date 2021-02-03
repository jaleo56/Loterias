import pandas as pd
from HojaExcel import HojaExcel
from settings import Settings

class Estadisticas:
    lAciertos = []
    lResumen = []
    resultadosRange = []

    def __init__(self, file, sheet, loto):
        self.s = Settings(file, sheet, loto)

    ########################################################################################
    # API
    #---------------------------------------------------------------------------------------

    def checkEstadisticas(self, updXLS=False):
        xls = self._getInfoFromExcel(tipo="APUESTAS")
        self.lEstadisticas = self._checkEstadisticas(self.apuestas)
        if updXLS:
            xls.publicarRango(self.s.COL_FIGURAS, self.lEstadisticas)
        else:
            print (self.lEstadisticas)


    ########################################################################################
    # MODULOS INTERNOS. NIVEL 1
    #---------------------------------------------------------------------------------------
    
    def _checkEstadisticas(self, dfCombis):
        lEstadisticas = []
        lRes          = []  
        print (f"{dfCombis=}")
        self._inicioArraysNumeros()
        
        for i, combi in dfCombis.iterrows():
            if i == 0: continue
        
            lf = self._checkFiguras(set(combi))
            ls = self._checkSeguidos(list(combi))
            ld = self._checkDistribucion(set(combi))
        
            lRes = lf
            lRes.extend(ls)
            lRes.extend(ld)

            lEstadisticas.append(lRes)    
        return lEstadisticas


    def _checkFiguras(self, sCombinacion):
        lFiguras = []
        pares       = len(sCombinacion.intersection(self.numerosPares))
        impares     = self.s.NUMS_COMBINACION - pares
        bajos       = len(sCombinacion.intersection(self.numerosBajos))
        altos       = self.s.NUMS_COMBINACION - bajos
        periferia   = len(sCombinacion.intersection(self.numerosPeriferia))
        centrales   = self.s.NUMS_COMBINACION - periferia

        lTerminaciones  = [0] * 11
        lDecenas        = [0] * 6
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

        fDecenas    = ""
        cntDecenas  = 0
        lDecenas.sort(reverse=True)
        for n in range(6):
            if lDecenas[n] > 0: 
                cntDecenas += 1
                fDecenas += str(lDecenas[n]) if fDecenas == "" else str("|") + str(lDecenas[n])
        print (f"{fDecenas=}")

        for n in range(10):
            if lIntervalos[n] > 0: lIntervalos[10] += 1

        lFiguras = [fDecenas, altos, bajos, pares, impares, periferia, centrales]
        lFiguras.extend(lTerminaciones)
        lFiguras.extend(lIntervalos)

        return lFiguras


    def _checkSeguidos(self, lCombinacion):
        lSeguidos = [0] * 7
        seg = 0
        for i in range(1, 6):
            if lCombinacion[i] - lCombinacion[i-1] == 1:
                seg += 1
            else:
                if seg > 0: lSeguidos[seg] += 1
                seg = 0
        else:
            if seg > 0: lSeguidos[seg] += 1 

        for i in range(6): 
            if lSeguidos[i] > 0: lSeguidos[6] += 1  
        
        return lSeguidos

    
    def _checkDistribucion(self, sCombinacion):
        lDistribucion = [0] * 9

        for x in range(len(self.s.GRUPOS_NUMS)):
            numeros = set(self.s.GRUPOS_NUMS[x])
            lDistribucion[x] = len(sCombinacion.intersection(numeros))  

        nGrupos = 0

        for na in lDistribucion:
            if na > 0: nGrupos += 1    

        lDistribucion[8] = nGrupos    
              
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

########################################################################################
# MACROS EXCEL
#---------------------------------------------------------------------------------------
def CheckEstadisticasMacroExcel(file, sheet, loto):
    std = Estadisticas(file, sheet, loto)
    std.checkEstadisticas(updXLS=True)

########################################################################################
# TEST LOCAL
#---------------------------------------------------------------------------------------
if __name__ == "__main__":
    CheckEstadisticasMacroExcel("Loterias.xlsm", "PRIMITIVA", "PRIMITIVA")
 