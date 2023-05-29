from flask import Flask,jsonify,request
import requests

app = Flask(__name__)

@app.route("/")
def elementos():
    elementos= []
    while len(elementos)<25:
        response = requests.get("https://api.chucknorris.io/jokes/random")
        
        if response.status_code==200:
            elemento = response.json()
            if elemento["id"] not in [i["id"] for i in elementos]:
                elementos.append(elemento)
    return jsonify(response=elementos)

app.run()

