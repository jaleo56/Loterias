def check():
    l = [1, 2, 3, 7, 8, 9]
    seguidos = [0] * 7
    seg = 0
    for i in range(1, 6):
        if l[i] - l[i-1] == 1:
            seg += 1
        else:
            if seg > 0: seguidos[seg] += 1
            seg = 0
    else:
        if seg > 0: seguidos[seg] += 1

    print (f"{seguidos=}")

def rango():
    for i in range(1,10):
        print (f"{i=}")

def seguidos():
    numant=5
    terminacion = numant % 10
    nFiguras=[[2, 6, 8, 10, 20], [12, 14, 16, 18, 22], [40, 46, 48], [34, 38, 26]]
    for i in range(len(nFiguras)):
        nFiguras[i] = [x for x in nFiguras[i] if int(x) != numant+1]
        nFiguras[i] = [x for x in nFiguras[i] if int(x) % 10 != terminacion]
    print (f"{numant=}. {nFiguras=}")

if __name__ == "__main__":
    seguidos()