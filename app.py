from flask import Flask, redirect, url_for
from pycoingecko import CoinGeckoAPI
from pymongo import MongoClient
import time

app = Flask(__name__)

cg = CoinGeckoAPI()
clientMongo = MongoClient('mongodb://localhost:27017')
db = clientMongo.crypto

coinListCollection = db.coinList


@app.route("/")
def index():
    return redirect(url_for('ping'))


@app.route("/ping")
def ping():
    return cg.ping()


@app.route("/coins/list", methods=['GET'])
def printCoinsList():
    return str(coinListCollection.find())


@app.route("/coins/list", methods=['POST'])
def updateCoinsList():
    coinListCollection.drop()
    for i in cg.get_coins_list():
        coinListCollection.insert_one(i)
    return redirect(url_for("/coins/list"))



