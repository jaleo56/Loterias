def potencia(c):
    """Calcula y devuelve el conjunto potencia del 
       conjunto c.
    """
    if len(c) == 0:
        return [[]]
    r = potencia(c[:-1])
    return r + [s + [c[-1]] for s in r]


def imprime_ordenado(c):
    """Imprime en la salida estándar todos los
       subconjuntos del conjunto c (una lista de
       listas) ordenados primero por tamaño y
       luego lexicográficamente. Cada subconjunto
       se imprime en su propia línea. Los
       elementos de los subconjuntos deben ser
       comparables entre sí, de otra forma puede
       ocurrir un TypeError.
    """
    for e in sorted(c, key=lambda s: (len(s), s)):
        print(e)


def combinaciones(c, n):
    """Calcula y devuelve una lista con todas las
       combinaciones posibles que se pueden hacer
       con los elementos contenidos en c tomando n
       elementos a la vez.
    """
    return [s for s in potencia(c) if len(s) == n]


if __name__ == "__main__":
    imprime_ordenado(
        # combinaciones(['0', '1', '2', '3', '4', '5', '6', '7'], 6))
        combinaciones(['pbp', 'pbc', 'pap', 'pac', 'ibp', 'ibc', 'iap', 'iac'], 6))



# ['pbc', 'pap', 'pac', 'ibp', 'ibc', 'iap']
# ['pbp', 'pap', 'pac', 'ibp', 'ibc', 'iac']
# ['pbp', 'pbc', 'pac', 'ibp', 'ibc', 'iap']
# ['pbp', 'pbc', 'pap', 'ibc', 'iap', 'iac']

# ['pap', 'pac', 'ibp', 'ibc', 'iap', 'iac']
# ['pbc', 'pac', 'ibp', 'ibc', 'iap', 'iac']
# ['pbc', 'pap', 'ibp', 'ibc', 'iap', 'iac']
# ['pbc', 'pap', 'pac', 'ibc', 'iap', 'iac']
# ['pbc', 'pap', 'pac', 'ibp', 'iap', 'iac']
# ['pbc', 'pap', 'pac', 'ibp', 'ibc', 'iac']
# ['pbc', 'pap', 'pac', 'ibp', 'ibc', 'iap']
# ['pbp', 'pac', 'ibp', 'ibc', 'iap', 'iac']
# ['pbp', 'pap', 'ibp', 'ibc', 'iap', 'iac']
# ['pbp', 'pap', 'pac', 'ibc', 'iap', 'iac']
# ['pbp', 'pap', 'pac', 'ibp', 'iap', 'iac']
# ['pbp', 'pap', 'pac', 'ibp', 'ibc', 'iac']
# ['pbp', 'pap', 'pac', 'ibp', 'ibc', 'iap']
# ['pbp', 'pbc', 'ibp', 'ibc', 'iap', 'iac']
# ['pbp', 'pbc', 'pac', 'ibc', 'iap', 'iac']
# ['pbp', 'pbc', 'pac', 'ibp', 'iap', 'iac']
# ['pbp', 'pbc', 'pac', 'ibp', 'ibc', 'iac']
# ['pbp', 'pbc', 'pac', 'ibp', 'ibc', 'iap']
# ['pbp', 'pbc', 'pap', 'ibc', 'iap', 'iac']
# ['pbp', 'pbc', 'pap', 'ibp', 'iap', 'iac']
# ['pbp', 'pbc', 'pap', 'ibp', 'ibc', 'iac']
# ['pbp', 'pbc', 'pap', 'ibp', 'ibc', 'iap']
# ['pbp', 'pbc', 'pap', 'pac', 'iap', 'iac']
# ['pbp', 'pbc', 'pap', 'pac', 'ibc', 'iac']
# ['pbp', 'pbc', 'pap', 'pac', 'ibc', 'iap']
# ['pbp', 'pbc', 'pap', 'pac', 'ibp', 'iac']
# ['pbp', 'pbc', 'pap', 'pac', 'ibp', 'iap']
# ['pbp', 'pbc', 'pap', 'pac', 'ibp', 'ibc']
