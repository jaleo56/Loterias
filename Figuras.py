from settings import Settings
from random   import randrange


class Figuras:

	def getFiguras(self, s, ndecenas=None):
		numeros = self._getNumerosAJugar(s, ndecenas)
		self._getBases(s, numeros)
		return(self._getGrupos())


	def _getNumerosAJugar(self, s, ndecenas=None):
		numeros = []
		if ndecenas == 0:    
			# 0. Seleccionar NUMEROS IMPARES
			numeros = [x for x in range(20, 44)]
			# numeros = [x for x in range(1, s.NUM_MAYOR  + 1) if x % 2 != 0]
		elif ndecenas == 0:
			# 1. Seleccionar TODOS LOS NUMEROS
			numeros = [x for x in range(1, s.NUM_MAYOR + 1)]	
		else:
			# 2. Seleccionar numeros de N DECENAS
			for x in range(ndecenas):
				y = s.DECENAS.pop(randrange(len(s.DECENAS)))
				numeros.extend([z for z in range((y*10), (y*10)+10)])
				print(f"{y=}")
		return numeros


	def _getBases(self, s, numeros):
		self.numerosPares      = set (x for x in numeros if x % 2 == 0)
		self.numerosImpares    = set([x for x in numeros if x % 2 != 0])
		self.numerosBajos      = set([x for x in numeros if x <= 25])
		self.numerosAltos      = set([x for x in numeros if x >  25])
		self.numerosPeriferia  = set(numeros).intersection(set(s.NUMS_PERIFERIA)) 
		self.numerosCentrales  = set(numeros).intersection(set(s.NUMS_CENTRALES))  


	def _getGrupos(self):
		pap = list(self.numerosPares.intersection(self.numerosAltos).intersection(self.numerosPeriferia))
		pac = list(self.numerosPares.intersection(self.numerosAltos).intersection(self.numerosCentrales))
		pbp = list(self.numerosPares.intersection(self.numerosBajos).intersection(self.numerosPeriferia))
		pbc = list(self.numerosPares.intersection(self.numerosBajos).intersection(self.numerosCentrales))
		iap = list(self.numerosImpares.intersection(self.numerosAltos).intersection(self.numerosPeriferia))
		iac = list(self.numerosImpares.intersection(self.numerosAltos).intersection(self.numerosCentrales))
		ibp = list(self.numerosImpares.intersection(self.numerosBajos).intersection(self.numerosPeriferia))
		ibc = list(self.numerosImpares.intersection(self.numerosBajos).intersection(self.numerosCentrales))
		print ("Pares-Altos-Periferia: ", pap)
		print ("Pares-Altos-Centrales: ", pac)
		print ("Pares-Bajos-Periferia: ", pbp)
		print ("Pares-Bajos-Centrales: ", pbc)
		print ("Impares-Altos-Periferia: ", iap)
		print ("Impares-Altos-Centrales: ", iac)
		print ("Impares-Bajos-Periferia: ", ibp)
		print ("Impares-Bajos-Centrales: ", ibc)

		ls = [pbp, pbc, pap, pac, ibp, ibc, iap, iac]
		lsn= [x for x in ls if len(x) > 0]
		return (lsn)


if __name__ == "__main__":
	s = Settings("Loterias2.xlsm", "PRIMITIVA")
	f = Figuras()
	ls = f.getFiguras(s, ndecenas=4)
	print (f"{ls=}")