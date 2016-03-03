# ~#~ coding: UTF-8 ~#~

u"""
En este archivo se encuentran las vistas de la aplicación.
"""

# Modules ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import gspread
import nltk.data
from flask import render_template
from flask import request
from oauth2client.client import SignedJwtAssertionCredentials
from datetime import datetime
import calendar

from . import app
from . import helpers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Views ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/', methods=['GET', 'POST'])
def index():
    text = helpers.convert('http://ir.eia.gov/wpsr/wpsrsummary.pdf').decode('unicode_escape').encode('ascii','ignore')

    if request.method == 'GET':
        return render_template('show.html', text=text)

    # Autorizar
    gc = gspread.authorize(SignedJwtAssertionCredentials(
        app.config['GS_AUTH']['client_email'],
        app.config['GS_AUTH']['private_key'].encode(),
        ['https://spreadsheets.google.com/feeds']
    ))
  
    # Procesar
    tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
    lineas=tokenizer.tokenize(text)
    words = nltk.word_tokenize(text)
    linea12 = lineas[12:13]
    linea12words = nltk.word_tokenize(linea12)
    week= u' '.join(words[7:11]).decode('unicode_escape').encode('ascii','ignore')
    linea1= u' '.join(lineas[8:10]+[', according to government data for the ']).decode('unicode_escape').encode('ascii','ignore')+week
    linea2= u' '.join(lineas[4:6]).decode('unicode_escape').encode('ascii','ignore')
    linea3= u' '.join(lineas[10:11]).decode('unicode_escape').encode('ascii','ignore')
    linea5= u' '.join(lineas[1:2]).decode('unicode_escape').encode('ascii','ignore')

    # Obtener datos de desempleo de googlesheet
    sht1 = gc.open_by_key(app.config['SPREADSHEET_ID'])
    worksheet1 = sht1.get_worksheet(0)
    worksheet2 = sht1.get_worksheet(1)
    worksheet3 = sht1.get_worksheet(2)
    calefaccion = worksheet1.acell('B11').value
    totalreservas = worksheet1.acell('B19').value
    totalreservasfino = '{:,}'.format(float(totalreservas))
    reservaschange = worksheet1.acell('E19').value
    verb = worksheet2.acell('A1').value
    wtidate = worksheet3.acell('A2').value
    mydate = datetime.strptime(wtidate,'%m/%d/%Y')
    month = calendar.month_name[mydate.month]
    wtiprice = worksheet3.acell('D2').value
    wtivariation = worksheet3.acell('E2').value
    linea4b= u' to a total of {} millions.'.format(calefaccion)
    palabra= 'Distillate'
    search = [i for i,x in enumerate(words) if x == palabra]
    position1= search[2]
    position2=position+10
    linea4= u' '.join(words[position1:position2]).decode('unicode_escape').encode('ascii','ignore')+linea4b
    linea6 = u'The total figure for oil reserves, including the Strategic Reserves, {} a total of {} million barrels, a {} percent change versus the previous week'.format(verb,totalreservasfino,reservaschange)
    linea7 = u'Right now, the price of the WTI Oil for {} is trading at {} dollars, a change of {} dollars'.format(month,wtiprice,wtivariation)
    return render_template('show.html', **dict(
        linea1=linea1,
        linea2=linea2,
        linea3=linea3,
        linea4=linea4,
        linea5 = linea5,
        linea6 = linea6,
        linea7 = linea7
    ))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
