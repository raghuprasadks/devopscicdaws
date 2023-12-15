'''
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST']) # To render Homepage
def home_page():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080) #for deployment run
    #app.run(host="127.0.0.1", port=8081,debug=True) # for local run
'''

import pickle

import numpy as np
from flask import Flask,request,render_template

app = Flask(__name__)

__model = None


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __model
    if __model is None:
        with open('./carmodel_4-dec-2023.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")

def get_estimated_price(mileage,age):
    x = np.zeros(2)
    x[0] = mileage
    x[1] = age
    return __model.predict([x])[0]


@app.route("/",methods=['GET'])
def welcome():
    return render_template('index.html')

@app.route("/carpriceapi",methods=['POST'])
def predictcarprice():
    mileage = request.form['mileage']
    age = request.form['age']
    
    price = get_estimated_price(int(mileage), int(age))
    print("price ",price)
    return render_template('index.html', predictedprice = int(price))
    

if(__name__=="__main__"):
    load_saved_artifacts()
    app.run(host="0.0.0.0", port=8080) #for deployment run
    #app.run(host="127.0.0.1", port=8082,debug=True) # for local run
    