from random import randrange
from HojaExcel import HojaExcel
from settings import Settings
from Figuras import Figuras
import copy

###################################################################################
#  Clase BomboNumeros     
#   . Extrae un numero del tipo solicitado: azar, pares, impares,...     
#   . Los numeros se borran del bombo a medida que se extraen
#   . El numero de apuestas máximo es 10x5 o 8x6
#   . El numero de estrellas se recrea cuando se agotan
###################################################################################
class BomboNumeros:

    def __init__(self, s):
        self.numerosAleatorios      = []
        self.numerosPares           = []
        self.numerosImpares         = []

        self.numerosInitPeriferia   = s.NUMS_PERIFERIA
        self.numerosInitCentrales   = s.NUMS_CENTRALES 
        self.numerosPeriferia       = []
        self.numerosCentrales       = []

        self.numerosBajos           = []
        self.numerosAltos           = []
        self.numerosIntervalos      = s.NUMS_INTERVALOS 
        self.numerosEstrellas       = []

        self.gruposAJugar           = []
        self.idxg                   = []
        self.nFiguras               = [0] * 8 * 8
        self.numsFiguras            = []

        # self._inicioArraysNumeros(s)


    def _inicioArraysNumeros(self, s):
        self.numerosAleatorios  = [x for x in range(1, s.NUM_MAYOR  + 1)]
        self.numerosPares       = [x for x in range(1, s.NUM_MAYOR  + 1) if x % 2 == 0]
        self.numerosImpares     = [x for x in range(1, s.NUM_MAYOR  + 1) if x % 2 != 0]
        self.numerosBajos       = [x for x in range(1, 26)]
        self.numerosAltos       = [x for x in range(26, s.NUM_MAYOR  + 1)]
        self.numerosPeriferia   = self.numerosInitPeriferia.copy()
        self.numerosCentrales   = self.numerosInitCentrales.copy()


    def getNumeroAlAzar(self, s):
        if len(self.numerosAleatorios) == 0:
            self.numerosAleatorios = [x for x in range(1, s.NUM_MAYOR  + 1)]
        return self.numerosAleatorios.pop(randrange(len(self.numerosAleatorios)))

    def getNumeroTerminacion(self, s, idx=0, terminacion=None):
        if terminacion != None:
            if idx == 0:
                self.numerosAleatorios.clear()
            else:
                self.numerosAleatorios = [x for x in self.numerosAleatorios if x % 10 != terminacion]
        return(self.getNumeroAlAzar(s))

    def getEstrellaAlAzar(self, s):
        if len(self.numerosEstrellas) == 0:
            self.numerosEstrellas = [x for x in range(1, s.NUMS_ESTRELLAS + 1)]
        return self.numerosEstrellas.pop(randrange(len(self.numerosEstrellas)))

    def getNumeroPar(self, s):
        if len(self.numerosPares) == 0:
            self.numerosPares = [x for x in range(1, s.NUM_MAYOR  + 1) if x % 2 == 0]
        return self.numerosPares.pop(randrange(len(self.numerosPares)))

    def getNumeroImpar(self, s):
        if len(self.numerosImpares) == 0:
            self.numerosImpares = [x for x in range(1, s.NUM_MAYOR  + 1) if x % 2 != 0]
        return self.numerosImpares.pop(randrange(len(self.numerosImpares)))

    def getNumeroBajo(self, s):
        if len(self.numerosBajos) == 0:
            self.numerosBajos = [x for x in range(1, 26)]
        return self.numerosBajos.pop(randrange(len(self.numerosBajos)))

    def getNumeroAlto(self, s):
        if len(self.numerosAltos) == 0:
            self.numerosAltos = [x for x in range(26, s.NUM_MAYOR  + 1)]
        return self.numerosAltos.pop(randrange(len(self.numerosAltos)))

    def getNumeroPeriferia(self, s):
        if len(self.numerosPeriferia) == 0:
            self.numerosPeriferia = self.numerosInitPeriferia.copy()
        return self.numerosPeriferia.pop(randrange(len(self.numerosPeriferia)))

    def getNumeroCentral(self, s):
        if len(self.numerosCentrales) == 0:
            self.numerosCentrales = self.numerosInitCentrales.copy()
        return self.numerosCentrales.pop(randrange(len(self.numerosCentrales)))

    def getIntervaloFromNumero(self, s, numero):
        intervalo = (i for i, e in enumerate(self.numerosIntervalos) if e >= numero)
        return next(intervalo)
        

    # ----- GRUPOS: BIP, BIC, BPP, BPC, AIP, AIC, APP, APC
    def getNumeroFiguras(self, s, idx, numant=0, ndecenas=0, ngrupos=3):

        # ---Seleccionar n grupos al azar (primera vez) 
        if len(self.gruposAJugar) == 0: 
            self.numsFiguras, self.gruposAJugar = self._createFiguras(s, ndecenas, ngrupos)     
            self.nFiguras = copy.deepcopy(self.numsFiguras)
            self.idxg     = copy.deepcopy(self.gruposAJugar)
            self.ng       = min(ngrupos, len(self.gruposAJugar))    

        # --- Seleccionar uno de los n grupos (sin repeticion) 
        if len(self.idxg) == 0:
            self.idxg = copy.deepcopy(self.gruposAJugar)
        # nGrupo = self.idxg.pop(randrange(len(self.idxg)))
        nGrupo = idx % self.ng

        # Borrar terminaciones y seguidos numero anterior
        if numant > 0:
            terminacion = numant % 10
            for i in range(len(self.nFiguras)):
                self.nFiguras[i] = [x for x in self.nFiguras[i] if x % 10 != terminacion]
                self.nFiguras[i] = [x for x in self.nFiguras[i] if x != numant]

        # --- Seleccionar numero del grupo seleccionado (sin repeticion: pop)
        if len(self.nFiguras[nGrupo]) == 0:
            self.nFiguras[nGrupo] = copy.deepcopy(self.numsFiguras[nGrupo])
        
        return self.nFiguras[nGrupo].pop(randrange(len(self.nFiguras[nGrupo])))
        

    def _createFiguras(self, s, ndecenas=0, ngrupos=0):
        gruposAJugar = []
        numsFiguras  = []

        # --- Obtener numeros de figuras
        f = Figuras()
        numsFiguras = f.getFiguras(s, ndecenas=ndecenas)

        # --- Seleccionar n grupos al azar
        grupos = copy.deepcopy(numsFiguras)
        gruSel = min(ngrupos, len(numsFiguras))    
        for x in range(gruSel):
            gruposAJugar.append(grupos.pop(randrange(len(grupos)))) 

        return numsFiguras, gruposAJugar 


###################################################################################
#  Clase Apuesta                                                         
#  Obtiene una apuesta del tipo de loteria jugado                            
###################################################################################
class Apuesta:
    def __init__(self, s):
        self.bombo = BomboNumeros(s)

    def obtenerApuesta(self, s):
        apuesta  = [0] * s.NUMS_COMBINACION 
        estrella = [0] * 2

        # OBTENER NUMEROS DE UNA APUESTA
        t = None
        apuestas_erroneas = 0
        found = False


        while not found:
            apuesta = [0] * s.NUMS_COMBINACION
            n = 0
            for i in range(s.NUMS_COMBINACION ):
                # # ---- NUMEROS DE N GRUPOS: BIP, BIC, BPP, BPC, AIP, AIC, APP, APC
                n = self.bombo.getNumeroFiguras(s, idx=i, numant=n, ndecenas=0, ngrupos=4)
                apuesta[i] = n 

                # ---- NUMEROS AL AZAR
                # apuesta[i] = self.bombo.getNumeroAlAzar(s)

                # ---- NUMEROS TERMINACIONES DIFERENTES
                # apuesta[i] = self.bombo.getNumeroTerminacion(s, idx=i, terminacion=t)
                # t = apuesta[i] % 10

                # ---- ALTERAR NUMEROS
                # if i == 0:
                #     apuesta[i] = self.bombo.getNumeroAlAzar()
                #
                # ---- ...(1) ALTOS Y BAJOS
                # elif ultimo < 26:                            
                #     apuesta[i] = self.bombo.getNumeroAlto()
                # else:
                #     apuesta[i] = self.bombo.getNumeroBajo()
                #
                # ---- ...(2) PERIFERIA Y CENTRALES
                # elif: ultimo in self.bombo.numerosInitPeriferia:
                #   apuesta[i] = self.bombo.getNumeroBajo()
                #
                # ultimo = apuesta[i]

            if len(apuesta) == len(set(apuesta)): 
                found = True
            else:
                apuestas_erroneas += 1

        print (f"{apuestas_erroneas=}")
        apuesta.sort()
        
        # OBTENER ESTRELLAS, si existen en el juego
        if s.NUMS_ESTRELLAS > 0:
            for i in range(2):
                estrella[i] = self.bombo.getEstrellaAlAzar(s)
            return apuesta + [0] + estrella
        else: 
            return apuesta + estrella 
                    
###################################################################################
#  Clase JuegoLoteria                                                    
#  Obtiene el conjunto de apuestas deseadas de una loteria.                  
###################################################################################
class Loteria: 
    def __init__(self, file, sheet): 
        self.s = Settings(file, sheet)
   
    def jugarLoteria(self, nApuestas, updXLS=False):
        apuestas = self._getApuestas(int(nApuestas))
        if updXLS:
            self._publicarExcel(apuestas)
        else:
            print (f"{apuestas=}")

    def _getApuestas(self, nApuestas):
        apuestas  = [[0] * self.s.NUMS_COMBINACION ] * nApuestas
        ap = Apuesta(self.s)
        for i in range(nApuestas):
            apuestas[i] = ap.obtenerApuesta(self.s)
        return apuestas
         
    def _publicarExcel(self, apuestas):
        xls = HojaExcel()
        xls.publicarRango(self.s.CEL_APUESTAS, apuestas)

####################################################################################
#  Macros excel                                                          
####################################################################################
def JugarMacroExcel(file, sheet, nApuestas):
    juego = Loteria(file, sheet)
    juego.jugarLoteria(nApuestas, updXLS=True)

###################################################################################
#  Test                                                                  
###################################################################################
if __name__ == "__main__":
    JugarMacroExcel("Test.xlsx", "PRIMITIVA", 16)
    

