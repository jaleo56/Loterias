import copy
from random import randrange
from HojaExcel import HojaExcel
from settings import Settings
from Figuras import Figuras
from utils import getDecenas, getFecha

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


    def getNumeroAlAzar(self, s, repetir=False):
        if len(self.numerosAleatorios) == 0:
            self.numerosAleatorios = [x for x in range(1, s.NUM_MAYOR  + 1)]
        if repetir:
            return self.numerosAleatorios[randrange(len(self.numerosAleatorios))]
        else:
            return self.numerosAleatorios.pop(randrange(len(self.numerosAleatorios)))

    def getNumeroTerminacion(self, s, numant=0):
        if numant == 0:
            self.numerosAleatorios.clear()
        else:
            t = numant % 10
            self.numerosAleatorios = [x for x in self.numerosAleatorios if x % 10 != t]
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


    # ----- GRUPOS: BIP, BIC, BPP, BPC, AIP, AIC, APP, APC
    def getNumeroFiguras(self, s, numant=0, ndecenas=0, ngrupos=0):

        # ---Seleccionar n grupos al azar (primera vez) 
        if len(self.gruposAJugar) == 0: 
            self.nFigurasJuego, self.gruposAJugar = self._createFiguras(s, ndecenas, ngrupos)     
            self.nFigurasApuesta = copy.deepcopy(self.nFigurasJuego)
            self.idxg            = copy.deepcopy(self.gruposAJugar)
            self.ng              = min(ngrupos, len(self.gruposAJugar))    

        # Borrar terminaciones y seguidos numero anterior
        if numant == 0:
            self.nFiguras = copy.deepcopy(self.nFigurasApuesta)        
        else:
            t = numant % 10
            for i in range(len(self.nFiguras)):
                self.nFiguras[i] = [x for x in self.nFiguras[i] if int(x) % 10 != t]
                self.nFiguras[i] = [x for x in self.nFiguras[i] if int(x) != numant+1]
                self.nFiguras[i] = [x for x in self.nFiguras[i] if int(x) != numant-1]
        
        # --- Seleccionar uno de los n grupos (sin repeticion) 
        if len(self.idxg) == 0:
            self.idxg = copy.deepcopy(self.gruposAJugar)
        nGrupo = self.idxg.pop(randrange(len(self.idxg)))
        # nGrupo = idx % self.ng

        # --- Seleccionar numero del grupo seleccionado (sin repeticion: pop)
        if len(self.nFiguras[nGrupo]) == 0:
            if len(self.nFigurasApuesta[nGrupo]) == 0:
                self.nFigurasApuesta[nGrupo] = copy.deepcopy(self.nFigurasJuego[nGrupo])
            self.nFiguras[nGrupo] = copy.deepcopy(self.nFigurasApuesta[nGrupo])
 
        n = self.nFiguras[nGrupo].pop(randrange(len(self.nFiguras[nGrupo])))
        self.nFigurasApuesta[nGrupo].remove(n)
        return n
        

    def _createFiguras(self, s, ndecenas=0, ngrupos=0):
        gruposAJugar = []
        numsFiguras  = []

        # --- Obtener numeros de figuras
        f = Figuras()
        numsFiguras = f.getFiguras(s, ndecenas=ndecenas)

        # --- Seleccionar n grupos al azar
        gruSel = min(ngrupos, len(numsFiguras))    
        g = [x for x in range(len(numsFiguras))]
        for x in range(gruSel):
            gruposAJugar.append(g.pop(randrange(len(g)))) 

        print (f"{numsFiguras=}")
        print (f"{gruposAJugar=}")
        return numsFiguras, gruposAJugar 


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


    def nums_al_azar(self, s, numant=None, ndecenas=None, ngrupos=None, repetir=False):
        return self.bombo.getNumeroAlAzar(s, repetir=repetir)


    def nums_term_dif(self, s, numant=0, ndecenas=None, ngrupos=None, repetir=None):
        return self.bombo.getNumeroTerminacion(s, numant=numant)


    def nums_figuras(self, s, numant=0, ndecenas=0, ngrupos=0, repetir=False):
        return self.bombo.getNumeroFiguras(s, numant=numant, ndecenas=ndecenas, ngrupos=ngrupos)


    def nums_alt_AltosBajos(self, s, numant=0, ndecenas=None, ngrupos=None, repetir=None):
        if numant == 0:
            return self.bombo.getNumeroAlAzar(s)        
        elif numant < 26:                            
            return self.bombo.getNumeroAlto(s)
        else:
            return self.bombo.getNumeroBajo(s)


    def nums_alt_PerfiCentrales(self, s, numant=0, ndecenas=None, ngrupos=None, repetir=None):
        if numant == 0:
            return self.bombo.getNumeroAlAzar(s)        
        elif numant in self.bombo.numerosInitPeriferia:
            return self.bombo.getNumeroBajo(s)
        else:
            return self.bombo.getNumeroBajo(s)


    def obtenerApuesta(self, s, fSelect, ndecenas=0, ngrupos=8, repetir=False):
        apuesta  = [0] * s.NUMS_COMBINACION 
        estrella = [0] * 2
        apuestas_erroneas = 0

        while True:
            # CREAR APUESTA
            apuesta = [0] * s.NUMS_COMBINACION
            numant = 0
            for i in range(s.NUMS_COMBINACION):
                apuesta[i] = fSelect(s, numant, ndecenas, ngrupos, repetir)
                numant = apuesta[i] 
            
            # OBTENER DECENAS APUESTA
            fDecenas = getDecenas(apuesta)

            # FILTRAR APUESTA: numeros y decenas
            if len(apuesta) == len(set(apuesta)):
                if fDecenas in s.LIST_DECENAS: break
            
            apuestas_erroneas += 1

        print (f"{apuestas_erroneas=}")
        apuesta.sort()
        
        # OBTENER ESTRELLAS, si existen en el juego
        if s.NUMS_ESTRELLAS > 0:
            for i in range(2):
                estrella[i] = self.bombo.getEstrellaAlAzar(s)
        return apuesta + estrella 
                    
###################################################################################
#  Clase JuegoLoteria                                                    
#  Obtiene el conjunto de apuestas deseadas de una loteria.                  
###################################################################################

class Loteria: 
    def __init__(self, file, sheet, loto): 
        self.s = Settings(file, sheet, loto)

    # --- API 
    def jugarLoteria(self, nApuestas, updXLS=False):
        apuestas = self._getApuestas(int(nApuestas))
        if updXLS:
            self._publicarExcel(apuestas)
        else:
            print (f"{apuestas=}")

    # --- UTILS MODULS
    def _getApuestas(self, nApuestas):
        apuestas  = [[0] * self.s.NUMS_COMBINACION ] * nApuestas
        ap = Apuesta(self.s)
        for i in range(nApuestas):
            # nums_al_azar, nums_term_dif, nums_figuras, nums_alt_AltosBajos, nums_alt_PerfiCentrales 
            apuestas[i] = ap.obtenerApuesta(self.s, ap.nums_figuras, ndecenas=0, ngrupos=8, repetir=False)
        return apuestas
         
    def _publicarExcel(self, apuestas):
        xls   = HojaExcel()
        fecha = getFecha()
        xls.publicarFecha(self.s.CEL_FECHA, fecha)
        xls.publicarRango(self.s.CEL_APUESTAS, apuestas)

####################################################################################
#  Macros excel                                                          
####################################################################################
def JugarMacroExcel(file, sheet, loto, nApuestas, updXLS=True):
    juego = Loteria(file, sheet, loto)
    juego.jugarLoteria(nApuestas, updXLS=updXLS)

def CheckNAnterioresMacroExcel(file, sheet):
    juego = Loteria(file, sheet)
    juego.checknanteriores(updxls="yes", nanteriores=7)

###################################################################################
#  Test                                                                  
###################################################################################
if __name__ == "__main__":
    JugarMacroExcel("Loterias.xlsm", "PRIMITIVA", "PRIMITIVA", 8, True)
    # CheckNAnterioresMacroExcel    ("Loterias.xlsm", "PRIMITIVA")
    

