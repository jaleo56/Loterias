from random import randrange
from HojaExcel import HojaExcel
from settings import Settings

###################################################################################
#  Clase BomboNumeros     
#   . Extrae un numero del tipo solicitado: azar, pares, impares,...     
#   . Los numeros se borran del bombo a medida que se extraen
#   . El numero de apuestas máximo es 10x5 o 8x6
#   . El numero de estrellas se recrea cuando se agotan
###################################################################################
class BomboNumeros:

    def __init__(self, s):
        self.numerosAleatorios = []
        self.numerosPares = []
        self.numerosImpares = []

        self.numerosInitPeriferia = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 20, 21, 30, 31, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
        self.numerosInitCentrales = [12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 27, 28, 29, 32, 33, 34, 35, 36, 37, 38, 39]
        self.numerosPeriferia = []
        self.numerosCentrales = []

        self.numerosBajos = []
        self.numerosAltos = []
        self.numerosIntervalos = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
        self.numerosEstrellas = []

        # self._inicioArraysNumeros(s)

    def _inicioArraysNumeros(self, s):
        self.numerosAleatorios = [x for x in range(1, s.NUM_MAYOR  + 1)]
        self.numerosPares = [x for x in range(1, s.NUM_MAYOR  + 1) if x % 2 == 0]
        self.numerosImpares = [x for x in range(1, s.NUM_MAYOR  + 1) if x % 2 != 0]
        self.numerosBajos = [x for x in range(1, 26)]
        self.numerosAltos = [x for x in range(26, s.NUM_MAYOR  + 1)]
        self.numerosPeriferia = self.numerosInitPeriferia.copy()
        self.numerosCentrales = self.numerosInitCentrales.copy()

    def getNumeroAlAzar(self, s, idx=0, terminacion=None):
        if terminacion != None:
            if idx == 0:
                self.numerosAleatorios.clear()
            else:
                self.numerosAleatorios = [x for x in self.numerosAleatorios if x % 10 != terminacion]
        if len(self.numerosAleatorios) == 0:
            self.numerosAleatorios = [x for x in range(1, s.NUM_MAYOR  + 1)]
        return self.numerosAleatorios.pop(randrange(len(self.numerosAleatorios)))

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

###################################################################################
#  Clase Apuesta                                                         
#  Obtiene una apuesta del tipo de loteria jugado                            
###################################################################################
class Apuesta:
    def __init__(self, s):
        self.bombo = BomboNumeros(s)

    def obtenerApuesta(self, s):
        apuesta = [0] * s.NUMS_COMBINACION 
        estrella = [0] * 2

        # Obtener numeros de 1 apuesta
        t = None
        for i in range(s.NUMS_COMBINACION ):
            apuesta[i] = self.bombo.getNumeroAlAzar(s, idx=i, terminacion=t)
            # print ("i: ", i, "numero: ", apuesta[i])
            # t = apuesta[i] % 10

            # if i == 0:
            #     apuesta[i] = self.bombo.getNumeroAlAzar()
            #     # ultimo = apuesta[i]
            # elif ultimo < 26:                            #ultimo in self.bombo.numerosInitPeriferia:
            #     apuesta[i] = self.bombo.getNumeroAlto()
            # else:
            #     apuesta[i] = self.bombo.getNumeroBajo()
            # ultimo = apuesta[i]

        # Obtener estrellas, si existen en el juego
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

    def jugarLoteria(self, nApuestas, updXLS=None):
        apuestas = self._getApuestas(int(nApuestas))
        if updXLS != None:
            self._publicarExcel(apuestas)

    def _getApuestas(self, nApuestas):
        apuestas  = [[0] * self.s.NUMS_COMBINACION ] * nApuestas
        combi = Apuesta(self)
        for i in range(nApuestas):
            apuestas[i] = combi.obtenerApuesta(self.s)
        return apuestas
         
    def _publicarExcel(self, apuestas):
        xls = HojaExcel()
        xls.publicarRango(self.s.CEL_APUESTAS, apuestas)

####################################################################################
#  Macros excel                                                          
####################################################################################
def JugarMacroExcel(file, sheet, nApuestas):
    juego = Loteria(file, sheet)
    juego.jugarLoteria(nApuestas, updXLS="yes")
    
###################################################################################
#  Test                                                                  
###################################################################################
if __name__ == "__main__":
    JugarMacroExcel("Loterias2.xlsm", "PRIMITIVA", 6)
    

