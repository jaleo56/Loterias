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
    def checkAciertos(self, updXLS=None):
        xls = self._getInfoFromExcel()      # Obtiene, apuestas, eApuestas, ganadoras,
        snApuestas = self._getNumsApuestas(self.apuestas)
        self.lAciertos = self._checkAciertos(self.ganadoras, snApuestas)
        if updXLS != None:
           xls.publicarColumna(self.s.CEL_ACIERTOS, self.lAciertos)


    def checkAllGanadoras(self, updXLS=None, resumir=None):
        xls = self._getInfoFromExcel()
        self.lAciertos, self.lResumen = self._checkGanadoras()
        if updXLS != None:
            resumen = [self.lResumen]
            for l in self.resultadosRange:
                resumen.append(l)
            if resumir == None:
                xls.publicarRango(self.s.CEL_RESULTADOS,  self.lAciertos)
            else:
                xls.publicarRango(self.s.CEL_RESUMEN, resumen)


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
 
    ########################################################################################
    # MODULOS INTERNOS. NIVEL 1
    #---------------------------------------------------------------------------------------
    def _checkAciertos(self, ganadoras, nssApuestas):
        lAciertos =[]
        for x, ganadora in ganadoras.iterrows():
            if x == 0: continue
            sGanadora = set(ganadora)
            naciertos = len(sGanadora.intersection(nssApuestas))
            lAciertos.append(naciertos)
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
        for ganadora in range(len(self.ganadorasRange)):
            sGanadora = set(ganadora)
            pares = len(sGanadora.intersection(self.numerosPares))
            impares = self.s.NUMS_COMBINACION - pares
            bajos = len(sGanadora.intersection(self.numerosBajos))
            altos = self.s.NUMS_COMBINACION - bajos
            periferia = len(sGanadora.intersection(self.numerosPeriferia))
            centrales = self.s.NUMS_COMBINACION - periferia

            lTerminaciones = [0] * 10
            for n in ganadora:
                lTerminaciones[n%10] += 1

            nTerminaciones = 0
            for n in range(10):
                if lTerminaciones[n] > 0: nTerminaciones += 1
            
            lFiguras.append([altos, bajos, pares, impares, periferia, centrales, lTerminaciones, nTerminaciones])    
        return lFiguras


    def _checkDistribucion(self):
        grupos = [ 
            {1, 3, 5, 7, 9, 11, 21}, 
            {13, 15, 17, 19, 23, 25},
            {2, 4, 6, 8, 10, 20}, 
            {12, 14, 16, 18, 22, 24}, 
            {41, 43, 45, 47, 49, 31}, 
            {33, 35, 37, 39, 27, 29},
            {40, 42, 44, 46, 48, 50, 30}, 
            {32, 34, 36, 38, 26, 28}] 
           
        lDistribucion = []
        for i in range(len(self.ganadoras)):
            sGanadora = set(self.ganadoras.iloc[i])
            ac = [0] * 9
            for x in range(len(grupos)):     
                numeros = set(grupos[x])
                ac[x] = len(sGanadora.intersection(numeros))  
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
                cntRow[30], cntRow[40], cntRow[41],
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
    std = Estadisticas()
    std.checkAciertos(updXLS="yes")

def CheckGanadorasMacroExcel(file, sheet):
    std = Estadisticas(file, sheet)
    std.checkAllGanadoras(updXLS="yes", resumir="yes")

def CheckFigurasMacroExcel(file, sheet):
    std = Estadisticas(file, sheet)
    std.checkFiguras(updXLS="yes")

########################################################################################
# TEST LOCAL
#---------------------------------------------------------------------------------------
if __name__ == "__main__":
    std = Estadisticas("Loterias2.xlsm", "PRIMITIVA")
    std.checkDistribucion("UPTXLS")

    # CheckGanadorasMacroExcel("Loterias2.xlsm", "PRIMITIVA")
    # CheckGanadorasMacroExcel("Loterias2.xlsm", "EUROMILLONES")
    # CheckFigurasMacroExcel("Loterias2.xlsm", "EUROMILLONES")
