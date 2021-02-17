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

        self.nsGruposJuego          = []

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

    def getNumeroFiguras(self, s, numant=0, ndecenas=0, ngrupos=0):

        # ---Crear figuras y seleccionar n grupos (primera vez) 
        if len(self.gruposAJugar) == 0: 
            self._createFiguras(s, ndecenas, ngrupos)     
 
        # Borrar terminaciones: anterior y siquiente numero anterior
        if numant == 0:
            self.nFiguras = copy.deepcopy(self.figurasApuesta)        
        else:
            t = numant % 10
            for i in range(len(self.nFiguras)):
                self.nFiguras[i] = [x for x in self.nFiguras[i] if int(x) % 10 != t]
                self.nFiguras[i] = [x for x in self.nFiguras[i] if int(x) != numant+1]
                self.nFiguras[i] = [x for x in self.nFiguras[i] if int(x) != numant-1]
        
        # --- Seleccionar grupo (sin repeticion) 
        if len(self.gruposApuesta) == 0:
            self.gruposApuesta = copy.deepcopy(self.gruposJuego)
        nGrupo = self.gruposApuesta.pop(randrange(len(self.gruposApuesta)))

        # --- Seleccionar numero del grupo seleccionado (sin repeticion)
        if len(self.nFiguras[nGrupo]) == 0:
            if len(self.figurasApuesta[nGrupo]) == 0:
                self.figurasApuesta[nGrupo] = copy.deepcopy(self.figurasJuego[nGrupo])
            self.nFiguras[nGrupo] = copy.deepcopy(self.figurasApuesta[nGrupo])
 
        n = self.nFiguras[nGrupo].pop(randrange(len(self.nFiguras[nGrupo])))
        # --- Eliminar numero seleccionado de numeros apuesta
        self.figurasApuesta[nGrupo].remove(n)
        return n
        
   
    def getNumeroNGrupos(self, s, ngrupos, numeros):
        # ---Crear n grupos de n numeros (primera vez) 
        if len(self.nsGruposJuego) == 0:
            self.cntNumeros      = 0
            self.nsGruposJuego   = self._createNGrupos(s, ngrupos, numeros)   
            self.nsGruposApuesta = copy.deepcopy(self.nsGruposJuego)

        nGrupo = int(self.cntNumeros / numeros)
        self.cntNumeros += 1
        
        # --- Seleccionar numero del grupo seleccionado (sin repeticion)
        print(f'{nGrupo=}')
        if len(self.nsGruposApuesta[nGrupo]) == 0:
            self.nsGruposApuesta[nGrupo] = copy.deepcopy(self.nsGruposJuego[nGrupo])
 
        # n = self.nsGruposApuesta[nGrupo].pop(randrange(len(self.nsGruposApuesta[nGrupo])))
        n = self.nsGruposApuesta[nGrupo].pop(0)

        return n 
    
    
    def _createFiguras(self, s, ndecenas=0, ngrupos=0):
        self.figurasJuego   = []
        self.figurasApuesta = [0] * 8 * 8
        self.gruposJuego    = []
        self.gruposApuesta  = []
        
        # --- Obtener numeros de figuras
        f = Figuras()
        self.figurasJuego = f.getFiguras(s, ndecenas=ndecenas)

        # --- Seleccionar n grupos al azar
        gruSel = min(ngrupos, len(self.figurasJuego))    
        g = [x for x in range(len(self.figurasJuego))]
        for x in range(gruSel):
            self.gruposJuego.append(g.pop(randrange(len(g)))) 

        self.figurasApuesta = copy.deepcopy(self.figurasJuego)
        self.gruposApuesta  = copy.deepcopy(self.gruposJuego)


    def _createNGrupos(self, s, ngrupos, numeros):
        nsGruposJuego   = []
        lGrupo          = [] 
        grupos_erroneos = 0
        iterGrupos      = 0
        cntCopys = 0 
        
        f = Figuras()
        figurasJuego    = f.getFiguras(s)
        nsFiguras       = copy.deepcopy(figurasJuego)
        
        for ng in range(ngrupos):
            while True:
                lGrupo = []
                for nn in range(numeros):
                    grupo = iterGrupos % len(figurasJuego)
                    if len(nsFiguras[grupo]) == 0:
                        nsFiguras[grupo] = copy.deepcopy(figurasJuego[grupo])
                        cntCopys += 1
                    num = nsFiguras[grupo].pop(randrange(len(nsFiguras[grupo])))
                    lGrupo.append(num)
                    iterGrupos += 1

                if len(lGrupo) == len(set(lGrupo)):
                    # lGrupo.sort()
                    nsGruposJuego.append(lGrupo)
                    break
                grupos_erroneos += 1
            
            print (f"{grupos_erroneos=}. {cntCopys=}")

        print(f'{nsGruposJuego=}')

        return nsGruposJuego

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
            
            # FILTRO DECENAS APUESTA
            fDecenas = getDecenas(apuesta)

            # FILTRAR APUESTA: numeros y decenas
            if len(apuesta) == len(set(apuesta)):
                # if fDecenas in s.LIST_DECENAS: 
                break
            
            apuestas_erroneas += 1

        print (f"{apuestas_erroneas=}")
        apuesta.sort()
        
        # OBTENER ESTRELLAS, si existen en el juego
        if s.NUMS_ESTRELLAS > 0:
            for i in range(2):
                estrella[i] = self.bombo.getEstrellaAlAzar(s)

        # UNION APUESTA + EXTRELLAS
        return apuesta + estrella 


    def nums_n_grupos(self, s, numant=0, ndecenas=0, ngrupos=3, repetir=False, agrupar=3):
        numeros = agrupar * s.NUMS_COMBINACION
        return self.bombo.getNumeroNGrupos(s, ngrupos, numeros)


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
            ng = int(nApuestas / 3)
            apuestas[i] = ap.obtenerApuesta(self.s, ap.nums_n_grupos, ndecenas=0, ngrupos=ng, repetir=False)
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

###################################################################################
#  Test                                                                  
###################################################################################
if __name__ == "__main__":
    JugarMacroExcel("Loterias.xlsm", "PRIMITIVA", "PRIMITIVA", 9, False)
    
