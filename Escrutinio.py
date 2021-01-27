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
        xls             = self._getInfoFromExcel("ALL")      # Obtiene, apuestas, eApuestas, ganadoras,
        snApuestas      = self._getNumsApuestas(self.apuestas)
        self.lAciertos  = self._checkAciertos(self.ganadoras, snApuestas)
        if updXLS:
            xls.publicarRango(self.s.CEL_ACIERTOS, self.lAciertos)
        else:
            print (f"{self.lAciertos=}")


    def checkAllGanadoras(self, updXLS=False, resumir=False):
        xls = self._getInfoFromExcel("ALL")     # Obtiene, apuestas, eApuestas, ganadoras,
        self.lAciertos, self.lResFila, self.lResumen = self._checkGanadoras()
        if updXLS:
            if resumir:
                resumen = [self.lResumen]
                for l in self.resultadosRange:
                    resumen.append(l)
                xls.publicarRango(self.s.CEL_RESUMEN, resumen)
            else:
                xls.publicarRango(self.s.CEL_RESUMEN, self.lResFila)
                # xls.publicarRango(self.s.CEL_RESULTADOS, self.lAciertos)
        else:
            print (f"{self.lAciertos=}")

    
    ########################################################################################
    # MODULOS INTERNOS. NIVEL 1
    #---------------------------------------------------------------------------------------
    def _checkAciertos(self, ganadoras, snApuestas):
        lAciertos =[]
        nNumeros = len(snApuestas)
        for x, ganadora in ganadoras.iterrows():
            if x == 0: continue
            sGanadora = set(ganadora)
            naciertos = len(sGanadora.intersection(snApuestas))
            lFila = [naciertos, nNumeros]
            lAciertos.append(lFila)
        return lAciertos


    def _checkGanadoras(self):
        lAciertos = []
        resumen   = []
        lResFila  = []
        # numsDifer = len(self._getNumsApuestas(self.apuestas))
        for x in range(len(self.ganadoras)):
            neRow = []
            cntRow = [0] * 61
            snGanadora = set(self.ganadoras.iloc[x])
            seGanadora = set(self.eGanadoras.iloc[x])
            # --- Get numeros y estrellas de las 10 ganadoras anteriores    
            # apuestas, estrellas = self._getApuestas(nganadora=x)
            for y in range(len(self.apuestas)):
                snApuesta = set(self.apuestas.iloc[y])
                seApuesta = set(self.eApuestas.iloc[y])
                nums = len(snGanadora.intersection(snApuesta))
                if self.s.LOTO == "PRIMITIVA":
                    # Check numero complementario
                    ests = len(seGanadora.intersection(snApuesta))
                else:
                    # Check estrellas
                    ests = len(seGanadora.intersection(seApuesta))
                neRow.append(nums)
                neRow.append(ests)
                cntRow[(nums*10)+ests] += 1
            for z in range(len(self.apuestas), 10):
                neRow.append("")
                neRow.append("")
            res = self._listaAciertos(cntRow)
            lAciertos.append(neRow + res)
            lResFila.append(res)
            resumen.append(res)

        total = pd.DataFrame(resumen).sum()
        lTotal = total.tolist()
        return lAciertos, lResFila, lTotal


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
    std = Escrutinio(file, sheet)
    std.checkAllGanadoras(updXLS=True, resumir=True)

########################################################################################
# TEST LOCAL
#---------------------------------------------------------------------------------------
if __name__ == "__main__":
    # AciertosMacroExcel            ("Test.xlsm", "PRIMITIVA")
    CheckGanadorasMacroExcel      ("Test.xlsm", "PRIMITIVA")
