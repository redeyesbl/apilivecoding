from flask import Flask, jsonify
import requests
import concurrent.futures

app = Flask(__name__)

@app.route("/")
def elementos():
    elementos =[]

    def obtener_elemento():
        response = requests.get("https://api.chucknorris.io/jokes/random")
        if response.status_code == 200:
            elemento = response.json()
            return elemento

    with concurrent.futures.ThreadPoolExecutor() as executor:
        while len(elementos) < 25:
            # Crear una lista de para realizar los requests 
            tasks = [executor.submit(obtener_elemento) for _ in range(25 - len(elementos))]

            # Esperar a que se completen todos los requests
            concurrent.futures.wait(tasks)

            # Obtener los resultados de los requests
            for task in tasks:
                if task.result():
                    elemento = task.result()
                    if elemento["id"] not in [i["id"] for i in elementos]:
                        elementos.append(elemento)

    #pequeño check que printea si hay o no hay ids repetidos
    if len([i["id"] for i in elementos])== len(set([i["id"] for i in elementos])):
        print("no hay ids repetidas")
    else:
        print("hay ids repetidos")

    return jsonify(response=list(elementos))

if __name__ == '__main__':
    app.run()