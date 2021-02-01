from datetime import datetime
import locale

locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))


def getFecha(sFecha):
    strFecha = sFecha[4:]
    strFecha = strFecha.replace('\xa0', ' ')
    dtFecha = datetime.strptime(strFecha, '%d %b %Y')
    return(dtFecha.date().strftime('%d/%m/%Y'))