'''
Created on 05/12/2014

@author: jaleo
'''
import re
import urllib2
from bs4 import BeautifulSoup
from xlwings import Workbook, Range


def obtenerResultados(hoja='Actual', wb=None):
    if wb is None:
       wb = Workbook()
    numq = 0          
    aciertos = ('U18','Z18','AE18')
    msg = 'RESULTADOS QUINIELA - {0} \n \n'.format(hoja)
    msg = msg + 'Distribucion = {0}-{1}-{2} \n'.format(int(Range(hoja,"T3").value), int(Range(hoja,"Y3").value), int(Range(hoja,"AD3").value))
    for quiniela in ('BD18','BU18','CL18'):        
        numq += 1
        msg = msg + '\n Q{0} ({1} Aciertos sin reducir) \n'.format(numq, int(Range(hoja,aciertos[numq-1]).value)) 
        l = Range(hoja, quiniela).table.value
        for n in range(9,15):
            msg = msg + '{0} Aciertos reales: {1} \n'.format(n, l.count(n))
    return msg


def obtenerIde():
    info = urllib2.urlopen('http://www.elgordo.com/results/quinises.asp?y=2015/16')
    soup = BeautifulSoup(info)
    lit1  = soup.find("table", { "class" : "tbl no-responsive qq" })
    ide = lit1.findAll('a')[0].get('href')
    ide = ide[-4:]
    # ide = str(int(ide)-1)
    return ide


def obtenerPremios(ide):
    msg = 'PREMIOS QUINIELA \n \n'
    info = urllib2.urlopen('http://www.elgordo.com/results/quinies.asp?sort=' + ide)
    soup = BeautifulSoup(info)
    all_rows  = soup.find("table", { "class" : "tbl no-responsive qq size80 tbl-result" })
    for i in range(0,6):
        cat = all_rows.findAll("td", { "data-title" : "Cat:"})[i].getText()
        ace = all_rows.findAll("td", { "data-title" : "Acertantes:"})[i].getText()
        pre = all_rows.findAll("td", { "data-title" : "Premios:"})[i].getText()
        pre = re.sub('\xa0', ' ', pre)
        pre = re.sub('\u20ac', 'E', pre)
        msg = msg + 'Cat: {0} \t Acertantes: {1} \t Premio: {2} \n'.format(cat, ace, pre.encode('utf-8'))
    return msg


def send_email(msge, dest=1):
    import smtplib
    import getpass

    # 1. Constants
    ME = 'josep.aleo@gmail.com'
    # USERS_WORK = ME
    USERS_WORK = ['rvillarbcn@gmail.com','051056@gmail.com','xavier.navarro.ale@gmail.com','franmena@gmail.com', ME]
    USERS_FAMILY = ['franc.aleo@gmail.com', 'davidaleo@hotmail.com', ME]
    SUBJECT = "Resultado quinielas de la semana"
    FROM = ME
    TEXT = msge
    gmail_user = ME  
    TO = USERS_WORK if dest == 1 else USERS_FAMILY
    TO = ME
    gmail_pwd = "1956estudio"
    # gmail_pwd = getpass.getpass(prompt='Enter gmail password: ')
    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        # server = smtplib.SMTP(SERVER)
        server = smtplib.SMTP("smtp.gmail.com", 587) # or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        # print 'successfully sent the mail'
    except:
        pass
        # print "failed to send mail"


def enviarResultados(hoja):
    message = obtenerResultados(hoja, None)
    ide = obtenerIde()
    premios = obtenerPremios(ide)
    msge = message + '\n \n' + premios
    send_email(msge, 1)


if __name__ == "__main__":
    PATH = r'/Users/jaleo/desktop/quinielas_wrk/1x2_working.xlsm'
    wb = Workbook(PATH)
    message = obtenerResultados('Actual', wb)
    print message
    '''
    ide = obtenerIde()
    premios = obtenerPremios(ide)
    msge = message + '\n \n' + premios
    send_email(msge, 2)
    print msge
    '''
