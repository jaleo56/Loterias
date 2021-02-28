import pandas as pd
from collections import Counter
from itertools import product
from HojaExcel import HojaExcel
from settings  import Settings

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
        print ("genera xls")
        self.lAciertos, self.lResFila, self.lResumen = self._checkGanadoras()
        print ("genera resultados")
        if updXLS:
            if resumir:
                resumen = [self.lResumen]
                for l in self.resultadosRange:
                    resumen.append(l)
                xls.publicarRango(self.s.CEL_RESUMEN, resumen)
            else:
                # xls.publicarRango(self.s.CEL_RESUMEN, self.lResFila)
                xls.publicarRango(self.s.CEL_RESULTADOS, self.lAciertos)
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


    def checkFrecuencias(self, nAnteriores):
        tot_apuestas, tot_premios, n = 0, 0, 0
        tot_aciertos = [0] * 8
        numsFreq = self._getAllNumsFreq()
        xls = self._getInfoFromExcel("GANADORAS")      
        for i in range(len(self.ganadoras)-nAnteriores):
            if (entra:=input('Quieres continuar ?')) in ("n", "no"): break 
            sGanadora    = set(self.ganadoras.iloc[i])
            sEstrellas   = set(self.eGanadoras.iloc[i])
            lnApuestas   = self._getApuestas(i, nAnteriores)
            aciertos     = self._checkAciertos(sGanadora, sEstrellas, lnApuestas)
            premio       = aciertos[7] * 500000 + aciertos[6] * 30000 + aciertos[5] * 2500 + aciertos[4] * 60 + aciertos[3] * 60 + aciertos[2] * 8
            tot_apuestas+= len(lnApuestas)
            tot_premios += premio
            for m in range(len(tot_aciertos)): 
                tot_aciertos[m] += aciertos[m]
            print(f'{sGanadora=}, {sEstrellas=}')
            print(f'Jornada: ', n:=n+1, f': {aciertos=}. {premio=}')
            print(f'TOTALES: {tot_aciertos=}. {tot_apuestas=}. {tot_premios=}')

    def checkEstadistica(self):
        cnt_apuestas, premios, n = 0, 0, 0
        aciertos_acum = [0] * 8
        xls = self._getInfoFromExcel("GANADORAS")      
        for i in range(len(self.ganadoras)-nAnteriores):
            if (entra:=input('Quieres continuar ?')) in ("n", "no"): break 
            sg = set(self.ganadoras.iloc[i])
            se = set(self.eGanadoras.iloc[i])
            lnApuestas = self._getApuestas(i, nAnteriores)
            aciertos   = self._checkApuestas(sg, se, lnApuestas)
            cnt_apuestas += len(lnApuestas)
            premios += aciertos[7] * 500000 + aciertos[6] * 30000 + aciertos[5] * 2500 + aciertos[4] * 60 + aciertos[3] * 60 + aciertos[2] * 8
            n += 1
            aciertos_acum += aciertos
            print(f'{list(self.ganadoras.iloc[i])=}, {se=}')
            print(f"{aciertos=}")
            print(f"{aciertos_acum=}")
            print(f'Número jornadas: {n}. {cnt_apuestas=}. {premios=}')


    def _getAllNumsFreq(self):
        nums = [x+1 for x in range(self.s.NUM_MAYOR)]
        return Counter(nums * 1000)
        # print(f'{numsFreq=}')
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
                if self.s.LOTO in ("BONOLOTO", "PRIMITIVA"):
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

    def _checkAciertos(self, snGanadora, seGanadora, lApuestas):
        cntRow = [0] * 61
        neRow  = []
        for apuesta in lApuestas:
            snApuesta = set(apuesta)
            nums = len(snGanadora.intersection(snApuesta))
            ests = len(seGanadora.intersection(snApuesta))
            neRow.append(nums)
            neRow.append(ests)
            cntRow[(nums*10)+ests] += 1
        res = self._listaAciertos(cntRow)
        return res


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

    def _getApuestas(self, i, nAnteriores):

        # 1.OBTENER LAS N-GANADORAS ANTERIORES A LA JUGADA, FILTRARLOS y ALINEARLOS EN 6 GRUPOS
        nApuestas = [[] for _ in range(6)]
        for j in range(1, nAnteriores+1):
            l = self.ganadoras.iloc[i+j].tolist()
            for x, n in enumerate(l):
                nested_list = nApuestas[x]
                nested_list.append(n)
        print(f"{nApuestas=}")


        # 2.OBTENER FRECUENCIAS DE LOS NUMEROS POR COLUMNA
        _count = [[] for _ in range(6)]
        for x in range(6):
            _count[x] = Counter(nApuestas[x])
        print(f'{_count=}')
            
        # 3.SELECCIONAR LAS N-FRECUENCIAS MAS ALTAS DE CADA COLUMNA
        elem  = [[] for _ in range(6)] 
        elems = [] 
        for x in range(6):
            elem = _count[x].most_common(2)
            elems.append(elem)
        print(f'{elems=}')
        
        # 4.EXTRAER EL NUMERO DE LA FRECUENCIA MAS ALTA
        elements = []
        for l in elems:
            lt = [t[0] for t in l]
            elements.append(lt)
        print(f'{elements=}')

        # 5.OBTENER PRODUCTO CARTESIANO TODAS LAS APUESTAS, FILTRAR APUESTAS ERRONEAS
        lApuestas = []
        apuestas_err = 0
        for apuesta in product(*elements):
            if len(apuesta) == len(set(apuesta)):
                lApuestas.append(apuesta)
                print(f'{apuesta=}')
            else:
                print(f'ERROR: {apuesta=}')
                apuestas_err += 1
        print(f'{apuestas_err=}')
            
        return lApuestas

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
        if self.s.LOTO in ("BONOLOTO", "PRIMITIVA"):
            return ([
                (
                cntRow[10] + cntRow[11]), 
                cntRow[20] + cntRow[21],
                cntRow[30] + cntRow[31], 
                cntRow[40], cntRow[41], cntRow[50], cntRow[51], cntRow[60]
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
    loto = "PRIMITIVA"
    std = Escrutinio(file, sheet, loto)
    std.checkAllGanadoras(updXLS=updXLS, resumir=False)

def CheckNAnterioresMacroExcel (file, sheet, loto, updXLS=True):
    esc = Escrutinio(file, sheet, loto)
    esc.checkNAnteriores(updXLS, nAnteriores=10, fuera=False)

def CheckFrecuenciasMacroExcel (file, sheet, loto, updXLS=False):
    esc = Escrutinio(file, sheet, loto)
    esc.checkFrecuencias(nAnteriores=100)

def CheckEstadisticaMacroExcel (file, sheet, loto):
    esc = Escrutinio(file, sheet, loto)
    esc.checkEstadistica()

########################################################################################
# TEST LOCAL
#---------------------------------------------------------------------------------------
if __name__ == "__main__":
    # AciertosGruposMacroExcel        ("Loterias.xlsm", "PRIMITIVA", "PRIMITIVA", True)
    # AciertosMacroExcel            ("Loterias.xlsm", "EUROMILLONES", "EUROMILLONES", True)
    # CheckGanadorasMacroExcel      ("Loterias.xlsm", "PRIMITIVA2", "PRIMITIVA", True)
    # CheckNAnterioresMacroExcel    ("Loterias.xlsm", "EUROMILLONES", "EUROMILLONES", True)
    CheckFrecuenciasMacroExcel     ("Loterias.xlsm", "BONOLOTO", "BONOLOTO")
    # CheckEstadisticaMacroExcel     ("Loterias.xlsm", "BONOLOTO", "BONOLOTO")
    
