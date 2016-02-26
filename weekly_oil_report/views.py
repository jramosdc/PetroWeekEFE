# ~#~ coding: UTF-8 ~#~

u"""
En este archivo se encuentran las vistas de la aplicación.
"""

# Modules ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import nltk.data
from flask import render_template
from flask import request
##from oauth2client.client import SignedJwtAssertionCredentials

from . import app
from . import helpers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Views ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/', methods=['GET', 'POST'])
def index():
    text = helpers.convert('http://ir.eia.gov/wpsr/wpsrsummary.pdf', pages=[0])

    if request.method == 'GET':
        return render_template('show.html', text=text)

    # Procesar
    tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
    lineas=tokenizer.tokenize(text)
    words = nltk.word_tokenize(text)
    week= u' '.join(words[7:11])
    linea1= u' '.join(lineas[8:10]+[', according to government data for the'])
    linea2= u' '.join(lineas[4:6])
    linea3= u' '.join(lineas[10:11]+lineas[12:13])
    linea4=u' '.join(lineas[1:2])

    return render_template('show.html', **dict(
        linea1=linea1,
        linea2=linea2,
        linea3=linea3,
        linea4=linea4
    ))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
