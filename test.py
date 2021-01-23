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

if __name__ == "__main__":
    rango()