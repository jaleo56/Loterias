import pandas as pd
from HojaExcel import HojaExcel
from settings import Settings

class Escrutinio:
    lAciertos = []
    lResumen = []
    resultadosRange = []

    def __init__(self, file, sheet):
        self.s = Settings(file, sheet)

    ########################################################################################
    # API
    #---------------------------------------------------------------------------------------
    def checkAciertos(self, updXLS=False):
        xls = self._getInfoFromExcel("ALL")      # Obtiene, apuestas, eApuestas, ganadoras,
        snApuestas = self._getNumsApuestas(self.apuestas)
        self.lAciertos = self._checkAciertos(self.ganadoras, snApuestas)
        if updXLS:
            xls.publicarRango(self.s.CEL_ACIERTOS, self.lAciertos)
        else:
            print (f"{self.lAciertos=}")


    def checkNAnteriores(self, updXLS=False, nAnteriores=10):
        xls = self._getInfoFromExcel("GANADORAS")      
        self.lAciertos = self._checkNAnteriores(nAnteriores)
        if updXLS:
           xls.publicarRango(self.s.CEL_ACIERTOS, self.lAciertos)
        else:
            print (f"{self.lAciertos=}")

    def checkAllGanadoras(self, updXLS=False, resumir=False):
        xls = self._getInfoFromExcel("ALL")     # Obtiene, apuestas, eApuestas, ganadoras,
        self.lAciertos, self.lResumen = self._checkGanadoras()
        if updXLS:
            resumen = [self.lResumen]
            for l in self.resultadosRange:
                resumen.append(l)
            if resumir:
                xls.publicarRango(self.s.CEL_RESUMEN, resumen)
            else:
                xls.publicarRango(self.s.CEL_RESULTADOS,  self.lAciertos)
        else:
            print (f"{self.lAciertos=}")
  
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
    

    ########################################################################################
    # MODULOS INTERNOS. NIVEL 2
    #---------------------------------------------------------------------------------------
    
    def _getInfoFromExcel(self, tipo="GANADORAS"):
        xls = HojaExcel()

        if tipo not in ("GANADORAS", "APUESTAS", "ALL"):
            raise Exception(f"Valor del parametro TIPO es erróneo. {tipo=}")

        if tipo in ("GANADORAS", "ALL"):
            ganadorasRange  = xls.getDataFrame(self.s.FILE_NAME, self.s.SHEET, self.s.RNG_GANADORAS)  
            self.ganadoras  = pd.DataFrame(ganadorasRange, columns=self.s.COLS_GANADORAS)
            self.eGanadoras = pd.DataFrame(ganadorasRange, columns=self.s.COLS_EGANADORAS )

        if tipo in ("APUESTAS", "ALL"):
            apuestasRange   = xls.getDataFrame(self.s.FILE_NAME, self.s.SHEET, self.s.RNG_APUESTAS)
            self.apuestas   = pd.DataFrame(apuestasRange, columns=self.s.COLS_APUESTAS)
            self.eApuestas  = pd.DataFrame(apuestasRange, columns=self.s.COLS_EAPUESTAS)

        if tipo in ("ALL"):
            self.resultadosRange = xls.getRange(self.s.FILE_NAME, self.s.SHEET, self.s.RNG_RESUMENES)
        
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
    std = Escrutinio(file, sheet)
    std.checkAciertos(updXLS=True)

def CheckGanadorasMacroExcel(file, sheet):
    std = Escrutinio(wfile, sheet)
    std.checkAllGanadoras(updXLS=True, resumir=True)

def CheckNAnterioresMacroExcel(file, sheet):
    std =Escrutinio(file, sheet)
    std.checkNAnteriores(updXLS="yes", nAnteriores=7)

########################################################################################
# TEST LOCAL
#---------------------------------------------------------------------------------------
if __name__ == "__main__":
    # AciertosMacroExcel            ("Test.xlsx", "PRIMITIVA")
    CheckGanadorasMacroExcel      ("Test.xlsx", "PRIMITIVA")
    # CheckNAnterioresMacroExcel    ("Loterias3.xlsm", "PRIMITIVA")