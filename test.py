def _inicioArraysNumeros():
        numerosAleatorios = set([x for x in range(1, 50 + 1)])
        numerosPares = set (x for x in range(1, 50 + 1) if x % 2 == 0)
        numerosImpares = set([x for x in range(1, 50 + 1) if x % 2 != 0])
        numerosBajos = set([x for x in range(1, 26)])
        numerosAltos = set (x for x in range(26, 50 + 1))
        numerosPeriferia = set ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 20, 21, 30, 31, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50])
        numerosCentrales = set ([12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 27, 28, 29, 32, 33, 34, 35, 36, 37, 38, 39])

        pap = numerosPares.intersection(numerosAltos).intersection(numerosPeriferia)
        print ("Pares-Altos-Periferia: ", pap)

        pac = numerosPares.intersection(numerosAltos).intersection(numerosCentrales)
        print ("Pares-Altos-Centrales: ", pac)

        pbp = numerosPares.intersection(numerosBajos).intersection(numerosPeriferia)
        print ("Pares-Bajos-Periferia: ", pbp)
        pbc = numerosPares.intersection(numerosBajos).intersection(numerosCentrales)
        print ("Pares-Bajos-Centrales: ", pbc)

        iap = numerosImpares.intersection(numerosAltos).intersection(numerosPeriferia)
        print ("Impares-Altos-Periferia: ", iap)
        iac = numerosImpares.intersection(numerosAltos).intersection(numerosCentrales)
        print ("Impares-Altos-Centrales: ", iac)

        ibp = numerosImpares.intersection(numerosBajos).intersection(numerosPeriferia)
        print ("Impares-Bajos-Periferia: ", ibp)
        ibc = numerosImpares.intersection(numerosBajos).intersection(numerosCentrales)
        print ("Impares-Bajos-Centrales: ", ibc)

        ls = [pbp, pbc, pap, pac, ibp, ibc, iap, iac]
        print (ls)

if __name__ == "__main__":
    _inicioArraysNumeros()
