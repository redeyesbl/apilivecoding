from flask import Flask, jsonify
import grequests
import time
from gevent import monkey
monkey.patch_all()
app = Flask(__name__)

@app.route('/')
def elementos():
    inicio =time.time()
    elementos = []
    joke_ids = set()
    urls = ['https://api.chucknorris.io/jokes/random'] * 25
    
    #crear las solicitudes grequests
    rs = (grequests.get(url) for url in urls)
    
    #enviar las solicitudes de manera asíncrona
    responses = grequests.map(rs)
    
    for response in responses:
        if response is not None and response.status_code == 200:
            elemento = response.json()
            joke_id = elemento['id']
            while joke_id in joke_ids:
                #si el ID ya existe, volvemos a realizar la solicitud
                response = grequests.get('https://api.chucknorris.io/jokes/random').send()
                if response is not None and response.status_code == 200:
                    elemento = response.json()
                    joke_id = elemento['id']
            
            joke_ids.add(joke_id)
            elementos.append(elemento)
    
    #función para chequear e imprimir en consola si se obtuvieron 25 IDs diferentes
    def check_unique_ids(jokes):
        unique_ids = len(set(elemento['id'] for elemento in elementos))
        if unique_ids == 25:
            print("Se obtuvieron 25 IDs diferentes.")
        else:
            print("No se obtuvieron 25 IDs diferentes. Se obtuvieron", unique_ids, "IDs únicos.")
    
    check_unique_ids(elementos)
    final = time.time()
    print(final-inicio)
    return jsonify(elementos)

if __name__ == '__main__':
    app.run()
