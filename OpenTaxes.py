#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, logging, requests, json
from werkzeug.exceptions import HTTPException
from flask import Flask, jsonify, make_response
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class OpenTaxes(Resource):



    def response(data, code):
        response = make_response(
            jsonify(
                {
                    'open_taxes': data
                }
            ),
            code,
        )
        response.headers["Content-Type"] = "application/json"
        return response


    @app.route("/api/v1/taxes/<string:taxname>/", methods=['GET'])
    @app.route("/api/v1/taxes/", methods=['GET'])
    def taxes(taxname = 'f'):
        if taxname is not None:

            dataTaxes = {
                'ipca': OpenTaxes.getIPCA(),
                'euro': OpenTaxes.getCurrency('euro'),
                'dolar': OpenTaxes.getCurrency('dolar'),
                'selic' : OpenTaxes.getSelic(),
            }

            try: 
                if taxname.lower() == 'f':
                    return OpenTaxes.response(dataTaxes, 200)
            except:
                return OpenTaxes.response({
                    'error' : 'Internal server error'
                }, 500)     
            
            try:
                return OpenTaxes.response({
                    taxname : dataTaxes[taxname]
                }, 200)
            except:
                return OpenTaxes.response({
                    'tax' : 'invalid tax name!'
                }, 500)
            



    def getSelic():
        try:
            jsonTaxes = json.loads(requests.get(os.getenv("SELIC_URL")).text)
            return str(jsonTaxes['conteudo'][0]['MetaSelic'])
        except:
            return OpenTaxes.response({
                'getSelic' : 'Internal eroor, check endpoint BCB.'
            }, 500)


    def getCurrency(currency):
        try:
            jsonTaxes = json.loads(requests.get(os.getenv("CURRENCY_URL")).text)

            dataDolar = {
                'compra' : str(jsonTaxes['conteudo'][0]['valorCompra']),
                'venda' : str(jsonTaxes['conteudo'][0]['valorVenda'])
            }
            
            dataEuro = {
                'compra' : str(jsonTaxes['conteudo'][2]['valorCompra']),
                'venda' : str(jsonTaxes['conteudo'][2]['valorVenda'])
            }
            
            if currency == 'dolar':
                return dataDolar
            
            return dataEuro
        except:
            return OpenTaxes.response({
                'getCurrency' : 'Internal eroor, check endpoint BCB.'
            }, 500)


    def getIPCA():
        try:
            jsonTaxes = json.loads(requests.get(os.getenv("IPCA_URL")).text)
            return str(jsonTaxes['conteudo'][0]['taxaInflacao'])
        except:
            return OpenTaxes.response({
                'getIPCA' : 'Internal eroor, check endpoint BCB.'
            }, 500)



    @app.errorhandler(HTTPException)
    def handle_exception(e):
        logging.basicConfig(filename='OpenTaxesError.log', level=logging.ERROR)
        error = {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
        logging.error(error)
        return OpenTaxes.response(error, e.code)


    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
