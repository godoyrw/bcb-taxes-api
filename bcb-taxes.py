#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, logging, requests, json
from queue import Empty
from werkzeug.exceptions import HTTPException
from flask import Flask, jsonify, make_response
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class BCBTaxes(Resource):

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


    @app.route("/api/v1/taxes/<string:taxname>/<string:taxattr>/", methods=['GET'])
    @app.route("/api/v1/taxes/<string:taxname>/", methods=['GET'])
    @app.route("/api/v1/taxes/", methods=['GET'])
    def taxes(taxname = 'f', taxattr = Empty):
        if taxname is not None:

            dataTaxes = {
                'ipca': BCBTaxes.getIPCA(),
                'euro': BCBTaxes.getCurrency('euro'),
                'dolar': BCBTaxes.getCurrency('dolar'),
                'selic' : BCBTaxes.getSelic(),
            }

            try: 
                if taxname.lower() == 'f':
                    return BCBTaxes.response(dataTaxes, 200)
            except:
                return BCBTaxes.response({
                    'error' : 'Internal server error'
                }, 500)     
            
            try:
                if taxattr is not Empty:
                    return BCBTaxes.response({
                        taxname : dataTaxes[taxname][taxattr]
                    }, 200)    
                return BCBTaxes.response({
                    taxname : dataTaxes[taxname]
                }, 200)
            except:
                return BCBTaxes.response({
                    'tax' : 'invalid tax name!'
                }, 500)
            



    def getSelic():
        try:
            jsonTaxes = json.loads(requests.get(os.getenv("SELIC_URL")).text)
            return str(jsonTaxes['conteudo'][0]['MetaSelic'])
        except:
            return BCBTaxes.response({
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
            return BCBTaxes.response({
                'getCurrency' : 'Internal eroor, check endpoint BCB.'
            }, 500)


    def getIPCA():
        try:
            jsonTaxes = json.loads(requests.get(os.getenv("IPCA_URL")).text)
            return str(jsonTaxes['conteudo'][0]['taxaInflacao'])
        except:
            return BCBTaxes.response({
                'getIPCA' : 'Internal eroor, check endpoint BCB.'
            }, 500)



    @app.errorhandler(HTTPException)
    async def handle_exception(e):
        logging.basicConfig(filename='BCBTaxesError.log', level=logging.ERROR)
        error = {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
        logging.error(error)
        return BCBTaxes.response(error, e.code)

    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
