from datetime import datetime, date
import locale

locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))


def getFecha(sFecha=None):
    if sFecha == None:
        today = date.today()
        return(today.strftime("%d/%m/%Y"))
    else:
        strFecha = sFecha[4:]
        strFecha = strFecha.replace('\xa0', ' ')
        dtFecha = datetime.strptime(strFecha, '%d %b %Y')
        return(dtFecha.date().strftime('%d/%m/%Y'))
    
 
def getDecenas(apuesta):
    lDecenas = [0] * 6
    fDecenas = ""
    for n in apuesta:
        d = int(n/10)-1 if n%10 == 0 else int(n/10)
        lDecenas[d] += 1
    lDecenas.sort(reverse=True)
    for n in lDecenas:
        if n > 0: 
            fDecenas += str(n) if fDecenas == "" else str("|") + str(n)
    # print(f"utils: {apuesta=}. {lDecenas=}. {fDecenas=}")
    return fDecenas
