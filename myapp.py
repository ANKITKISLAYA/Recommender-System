# -*- coding: utf-8 -*-

"""
Created on Tue Jan 10 15:25:15 2020

@author: Ankit kislaya
"""


# In this Programme i am creating flask application and Api's



import flask
from flask import request, jsonify, url_for
import json
import requests
import urllib.parse
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np
import copy
from datetime import datetime




import sys
import base64
import pandas as pd
from flask import Response
import json
from collections import Counter
import warnings
warnings.filterwarnings("ignore")


from RecSys import RecSys
from RecSys2 import RecSys2
from InsertRecSys import InsertRecSys



 # using sentry to generate log files in cloud
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

app = flask.Flask(__name__)
app.debug = True


sentry_sdk.init(
    dsn="https://d4f55392a9aa4f78a816e498c88fb5c3@sentry.io/1873356",
    integrations=[FlaskIntegration()]
)





class PrefixMiddleware(object):
#class for URL sorting
    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        #in this line I'm doing a replace of the word flaskredirect which is my app name in IIS to ensure proper URL redirect
        if environ['PATH_INFO'].lower().replace('/flaskredirect','').startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'].lower().replace('/flaskredirect','')[len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]


app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/foo')



	
	



@app.route('/recsysitem')
def recsysitem():
    
    itemid = request.args['itemid']
    number = request.args['number']
    
    jso=RecSys().rec(itemid,number)
    return jsonify(jso)
	




@app.route('/recsysitem1')
def recsysitem1():
    
    itemid = request.args['itemid']
    number = request.args['number']
    wid = request.args['warehouseid']
    jso=RecSys1().rec(itemid,number,wid)
    return jsonify(jso)





@app.route('/recsysitem2')
def recsysitem2():
    
    itemid = request.args['itemid']
    number = request.args['number']
    wid = request.args['warehouseid']
    jso=RecSys2().rec(itemid,number,wid)
    return jsonify(jso)





@app.route('/insertmatrix')
def insertmatrix():
    
    df1 = InsertRecSys().read()
    df2 = InsertRecSys().ExtractItemid(df1)
    df3 = InsertRecSys().Clean(df2)
    df4 = InsertRecSys().AddRating(df3)
    df5 = InsertRecSys().RenameColumns(df4)
    ltup = InsertRecSys().CosineSimilarityMatrix(df5)
    finalfreq = InsertRecSys().finalfreq(ltup)

    SimMat = ltup[0]
    lv = list(finalfreq.values())
    lc = list(finalfreq.keys())
    SimMat1 = lv * SimMat
    df_final = pd.DataFrame(SimMat1, columns = lc , index = lc)
    df_columns = df_final.columns.astype(str)
    lcolumn = list(df_columns)
    df1 = pd.DataFrame(df_final.values , columns = lcolumn , index = lcolumn)
    df1.reset_index(inplace=True,drop = True)
    lcolumn = [int(i) for i in lcolumn]
    df1.insert(0,"itemid",lcolumn)
    InsertRecSys().insertdata(df1)
    return ("Data Inserted")





    
    


if __name__ == '__main__':
    app.run()
