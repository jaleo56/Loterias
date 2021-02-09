import pandas as pd
# import numpy  as np
import xlwings as xw
from settings import Settings

class HojaExcel:

    def getDataFrame(self, wb_file, sheet, rangoin):
        rango = self.getRange(wb_file, sheet, rangoin)
        df=pd.DataFrame(rango)
        df.columns = df.iloc[0]
        df = df[1:]
        df = df.astype('int')
        # Data=Data.dropna(how='all',axis=1)
        # Data=Data.dropna(how='all',axis=0)
        return df

    def getRange(self, wb_file, sheet, rangoin):
        wb = xw.books(wb_file)
        last_row = wb.sheets[sheet].range(rangoin[0]).end('down').row
        rango=wb.sheets[sheet].range(f"{rangoin[0]}:{rangoin[1]}{last_row}").value
        return rango

    def publicarRango(self, rango, lista):
        xw.Range(rango).value = lista


    def publicarFecha(self, rango, fecha):
        if fecha != None:
           xw.Range(rango).value = fecha


    def publicarColumna(self, rango, lista):
        # lRow = len(lista)
        # xw.Range(f"{rango}:{rango[0]}{lRow}").clear_contents()
        xw.Range(rango).options(transpose=True).value = lista


if __name__ == "__main__":
    xls = HojaExcel()
    s = Settings("Loterias.xlsm", "PRIMITIVA", "PRIMITIVA")
    apuestasRange = xls.getDataFrame(s.FILE_NAME, s.SHEET, s.RNG_APUESTAS)
    apuestas  = pd.DataFrame(apuestasRange, columns=s.COLS_APUESTAS)
    estrellas = pd.DataFrame(apuestasRange, columns=s.COLS_EAPUESTAS)
    print (f"{apuestasRange=}")
    print (f"{apuestasRange.dtypes=}")