class Settings:
    RNG_GANADORAS          = ["B1", "I"]
    RNG_APUESTAS           = ["J1", "Q"]
    
    CEL_ACIERTOS           = "R2"
    CEL_RESULTADOS         = "S2"
    CEL_RESUMEN            = "AM2"
    CEL_APUESTAS           = "J2"

    def __init__(self, file, sheet):
        self.FILE_NAME               = file
        self.SHEET                   = sheet
        self.LOTO                    = sheet

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

        elif self.LOTO == "PRIMITIVA":
            self.NUM_MAYOR           = 49
            self.NUMS_COMBINACION    = 6
            self.NUMS_ESTRELLAS      = 0
            self.COLS_GANADORAS      = ['N1', 'N2', 'N3', 'N4', 'N5', 'N6']
            self.COLS_EGANADORAS     = ['C']
            self.COLS_APUESTAS       = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']
            self.COLS_EAPUESTAS      = ['C']
            self.RNG_RESUMENES       = ["AM2", "AR"]
            self.COL_FIGURAS         = "BA2"
            self.COL_DISTRIBUCION    = "AY2"

        elif self.LOTO == "ONCE":
            self.NUM_MAYOR           = 50
            self.NUMS_COMBINACION    = 5
            self.NUMS_ESTRELLAS      = 10
        else:
            raise ValueError("El tipo de loteria (nombre hoja) no está permitido.")


