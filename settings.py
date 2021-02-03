from array import *


class Settings:
    RNG_GANADORAS          = ["B2", "I"]
    RNG_APUESTAS           = ["K2", "R"]
    
    CEL_ACIERTOS           = "T3"
    CEL_RESULTADOS         = "AP3"
    CEL_RESUMEN            = "AP3"
    CEL_APUESTAS           = "K3"

    apuestas_cell = {
        "DASHBOARD_EUROMILLONES"    : "Q10",
        "DASHBOARD_PRIMITIVA"       : "H10",
        "PRIMITIVA_PRIMITIVA"       : "K3",
        "EUROMILLONES_EUROMILLONES" : "K3" 
    }

    # ----- GRUPOS: BIP, BIC, BPP, BPC, AIP, AIC, APP, APC
    GRUPOS_NUMS = [ 
        [1, 3, 5, 7, 9, 11, 21], 
        [13, 15, 17, 19, 23, 25],
        [2, 4, 6, 8, 10, 20], 
        [12, 14, 16, 18, 22, 24], 
        [41, 43, 45, 47, 49, 31], 
        [33, 35, 37, 39, 27, 29],
        [40, 42, 44, 46, 48, 50, 30], 
        [32, 34, 36, 38, 26, 28]] 
    
    NUMS_PERIFERIA = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 20, 21, 30, 31, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    NUMS_CENTRALES = [12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 27, 28, 29, 32, 33, 34, 35, 36, 37, 38, 39]
    NUMS_INTERVALOS= [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]


    def __init__(self, file, sheet, loto):
        self.FILE_NAME               = file
        self.SHEET                   = sheet
        self.LOTO                    = loto

        self.CEL_APUESTAS = self.apuestas_cell.get(sheet + "_" + loto, "E001: Invalid sheet or loto")
 
        if self.LOTO == "EUROMILLONES":
            self.NUM_MAYOR           = 50
            self.NUMS_COMBINACION    = 5
            self.NUMS_ESTRELLAS      = 12
            self.COLS_GANADORAS      = ['N1', 'N2', 'N3', 'N4', 'N5']
            self.COLS_EGANADORAS     = ['L1', 'L2']
            self.COLS_APUESTAS       = ['A1', 'A2', 'A3', 'A4', 'A5']
            self.COLS_EAPUESTAS      = ['E1', 'E2']
            self.RNG_RESUMENES       = ["AM2", "AZ"]
            self.COL_FIGURAS         = "BA2"
            self.COL_DISTRIBUCION    = "AY2"
            self.DECENAS             = [0, 1, 2, 3, 4, 5]
            

        elif self.LOTO == "PRIMITIVA":
            self.NUM_MAYOR           = 49
            self.NUMS_COMBINACION    = 6
            self.NUMS_ESTRELLAS      = 0
            self.COLS_GANADORAS      = ['N1', 'N2', 'N3', 'N4', 'N5', 'N6']
            self.COLS_EGANADORAS     = ['C']
            self.COLS_APUESTAS       = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']
            self.COLS_EAPUESTAS      = ['C']
            self.RNG_RESUMENES       = ["AP3", "AU"]
            self.COL_FIGURAS         = "AV3"
            self.COL_DISTRIBUCION    = "CC3"
            self.NUMS_PERIFERIA.remove(50)
            self.GRUPOS_NUMS[6].remove(50)
            self.NUMS_INTERVALOS.remove(50)
            self.DECENAS             = [0, 1, 2, 3, 4]
            self.COL_SEGUIDOS        = "BV3"

        elif self.LOTO == "ONCE":
            self.NUM_MAYOR           = 50
            self.NUMS_COMBINACION    = 5
            self.NUMS_ESTRELLAS      = 10
        else:
            raise ValueError("El tipo de loteria (nombre hoja) no está permitido.")

        self.NUMEROS_LOTO = [x for x in range(1, self.NUM_MAYOR  + 1)]


if __name__ == "__main__":
    s = Settings("Loterias3.xlsm", "PRIMITIVA")
    print (s.GRUPOS_NUMS)   


