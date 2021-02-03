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


def _checkSeguidos(lCombinacion):
        lSeguidos = [0] * 7
        seg = 0
        for i in range(1, 6):
            if lCombinacion[i] - lCombinacion[i-1] == 1:
                seg += 1
            else:
                if seg > 0: lSeguidos[seg] += 1
                seg = 0
        else:
            if seg > 0: lSeguidos[seg] += 1 

        for i in range(6): 
            if lSeguidos[i] > 0: lSeguidos[6] += 1  
        
        return lSeguidos

# from datetime import datetime
# import locale

# locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))

from utils import getFecha

def fecha():
    jornadaDate='sa,\xa030\xa0ene\xa02021'
    print(getFecha(jornadaDate))

    # jornadaDate = jornadaDate[:2] + jornadaDate[2:]    
    # jornadaDate = _publicarData(jornadaDate[4:])
    # print(f"{jornadaDate=}")

    # Convertimos un string con formato
    # <día> del <mes> de <año> a las <hora>:<minutos> en datetime
    # una_fecha = '20 del 04 de 2019 a las 12:00'
    # fecha_dt = datetime.strptime(jornadaDate, '%d %b %Y')
    # print(fecha_dt.date().strftime('%d/%m/%Y'))


    # from datetime import datetime
    # import locale

    # locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))

    # jornadaDate = jornadaDate[4:]
    # jornadaDate = jornadaDate.replace('\xa0', ' ')
    # fecha_dt = datetime.strptime(jornadaDate, '%d %b %Y')
    # fecha = fecha_dt.date().strftime('%d/%m/%Y')


# def _publicarData(txt):
#     txt = txt.replace('\xa0', ' ')
#     # txt.encode('utf-8')
#     #txt = re.sub('\xa0', ''.encode('utf-8'), txt)
#     return txt

def sw(sheet, loto):
    apuestas_cell = {
        "DASHBOARD_EUROMILLONES"    : "Q10",
        "DASHBOARD_PRIMITIVA"       : "H10",
        "PRIMITIVA_PRIMITIVA"       : "K3",
        "EUROMILLONES_EUROMILLONES" : "K3" 
    }
    print(apuestas_cell.get(sheet + "_" + loto, "E001: Invalid sheet or loto"))

if __name__ == "__main__":
    # s = _checkSeguidos([16, 20, 31, 32, 35, 48])
    # print(s)
    # fecha()
    sw("PRIMITIVA", "PRIMITIVAS")