import pandas as pd
from HojaExcel import HojaExcel
from settings import Settings

class Escrutinio:
    lAciertos = []
    lResumen = []
    resultadosRange = []

    def __init__(self, file, sheet, loto):
        self.s = Settings(file, sheet, loto)

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


    def checkAciertosGrupos(self, updXLS=False):
        xls             = self._getInfoFromExcel("ALL")      # Obtiene, apuestas, eApuestas, ganadoras,
        self.lAciertos  = self._checkAciertosGrupos(self.ganadoras, self.apuestas)
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

     
    def checkNAnteriores(self, updXLS=False, nAnteriores=10, fuera=True):
        print(f"{nAnteriores=}")
        xls = self._getInfoFromExcel("GANADORAS")      
        self.lAciertos = self._checkNAnteriores(nAnteriores, fuera)
        if updXLS:
           xls.publicarRango(self.s.CEL_ACIERTOS, self.lAciertos)
        else:
            print (f"{self.lAciertos=}") 
    
    ########################################################################################
    # MODULOS INTERNOS. NIVEL 1
    #---------------------------------------------------------------------------------------
    def _checkAciertos(self, ganadoras, snApuestas):
        lAciertos =[]
        nNumeros = len(snApuestas)
        print(f"{snApuestas=}")
        for x, ganadora in ganadoras.iterrows():
            if x == 0: continue
            sGanadora = set(ganadora)
            naciertos = len(sGanadora.intersection(snApuestas))
            lFila = [naciertos, nNumeros]
            lAciertos.append(lFila)
        return lAciertos


    def _checkAciertosGrupos(self, ganadoras, apuestas):
        lAciertos   = []
        lGrupos     = []
        flat_list   = []

        alist = apuestas.values.tolist()
        for i, a in enumerate(alist):
            flat_list.extend(a)
            if i>0 and i%3 == 2:
                lGrupos.append(flat_list)
                flat_list = []

        for x, ganadora in ganadoras.iterrows():
            if x == 0: continue
            sGanadora  = set(ganadora)
            acGanadora = []
            for ag in lGrupos:
                sApuestas = set(ag)
                nNumeros = len(sApuestas)
                naciertos = len(sGanadora.intersection(sApuestas))
                acGanadora.append(naciertos)
            acGanadora.sort(reverse=True)
            fAciertos = ""
            for n in acGanadora:
                fAciertos += str(n) if fAciertos == "" else str("|") + str(n)
            lFila = [fAciertos, nNumeros]
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


    def _checkNAnteriores(self, nAnteriores=7, fuera=True):
        nApuestas = []
        lAciertos = []
        cApuestas = []
        print(f"{nAnteriores=}")
        for i in range(len(self.ganadoras)-nAnteriores):
            sGanadora = set(self.ganadoras.iloc[i])
            nApuestas.clear()    
            for j in range(1,nAnteriores+1):
                l = self.ganadoras.iloc[i+j].tolist()
                nApuestas += l
            if fuera:
                cApuestas = [x for x in self.s.NUMEROS_LOTO if x not in nApuestas]
                sApuestas = set(cApuestas)
            else:
                sApuestas = set(nApuestas)
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
            # print(f"{self.ganadoras=}")
        
        if tipo in ("APUESTAS", "ALL"):
            apuestasRange   = xls.getDataFrame(self.s.FILE_NAME, self.s.SHEET, self.s.RNG_APUESTAS)
            self.apuestas   = pd.DataFrame(apuestasRange, columns=self.s.COLS_APUESTAS)
            self.eApuestas  = pd.DataFrame(apuestasRange, columns=self.s.COLS_EAPUESTAS)
            # print(f"{self.apuestas=}")

        if tipo in ("ALL"):
            self.resultadosRange = xls.getRange(self.s.FILE_NAME, self.s.SHEET, self.s.RNG_RESUMENES)
        
        return xls


    def _getNumsApuestas(self, apuestas):
        alist = apuestas.values.tolist()
        flat_list = [item for sublist in alist for item in sublist]
        return set(flat_list)
  

    def _listaAciertos(self, cntRow):
        if self.s.LOTO == "PRIMITIVA":
            return ([
                (cntRow[30] + cntRow[31]), cntRow[40], cntRow[41],
                cntRow[50], cntRow[51], cntRow[60]
            ])
        else:
            return ([
                cntRow[12], 
                cntRow[20], cntRow[21], cntRow[22],
                cntRow[30], cntRow[31], cntRow[32],
                cntRow[40], cntRow[41], cntRow[42],
                cntRow[50], cntRow[51], cntRow[52]
            ])


########################################################################################
# MACROS EXCEL
#---------------------------------------------------------------------------------------
def AciertosMacroExcel(file, sheet, loto, updXLS=True):
    std = Escrutinio(file, sheet, loto)
    std.checkAciertos(updXLS=True)

def AciertosGruposMacroExcel(file, sheet, loto, updXLS=True):
    std = Escrutinio(file, sheet, loto)
    std.checkAciertosGrupos(updXLS=updXLS)

def CheckGanadorasMacroExcel(file, sheet, loto, updXLS=True):
    std = Escrutinio(file, sheet, loto)
    std.checkAllGanadoras(updXLS=updXLS, resumir=True)

def CheckNAnterioresMacroExcel (file, sheet, loto, updXLS=True):
    esc = Escrutinio(file, sheet, loto)
    esc.checkNAnteriores(updXLS, nAnteriores=10, fuera=False)

########################################################################################
# TEST LOCAL
#---------------------------------------------------------------------------------------
if __name__ == "__main__":
    # AciertosGruposMacroExcel        ("Loterias.xlsm", "PRIMITIVA", "PRIMITIVA", True)
    # AciertosMacroExcel            ("Loterias.xlsm", "EUROMILLONES", "EUROMILLONES", True)
    CheckGanadorasMacroExcel      ("Loterias.xlsm", "PRIMITIVA", "PRIMITIVA", True)
    # CheckNAnterioresMacroExcel    ("Loterias.xlsm", "EUROMILLONES", "EUROMILLONES", True)
    