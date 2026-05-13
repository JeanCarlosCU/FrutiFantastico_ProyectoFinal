from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import certifi

app = Flask(__name__)



url = "mongodb+srv://frutiAdmin:Cetis#61@cluster0.rfqjfus.mongodb.net/?appName=Cluster0"

cliente = MongoClient(
    url,
    tlsCAFile=certifi.where()
)

db = cliente["FrutiFantasticoDB"]



usuarios = db["usuarios"]
clientes = db["clientes"]
productos = db["productos"]



if usuarios.count_documents({}) == 0:
    usuarios.insert_one({
        "usuario": "frutiAdmin",
        "password": "Cetis#61"
    })

@app.route("/", methods=["GET", "POST"])
def login():

    mensaje = ""

    if request.method == "POST":

        usuario = request.form["usuario"]
        password = request.form["password"]

        usuario_encontrado = usuarios.find_one({
            "usuario": usuario,
            "password": password
        })

        if usuario_encontrado:
            return redirect(url_for("dashboard"))

        else:
            mensaje = "Usuario o contraseña incorrectos"

    return render_template(
        "login.html",
        mensaje=mensaje
    )



@app.route("/dashboard")
def dashboard():

    lista_clientes = list(clientes.find())
    lista_productos = list(productos.find())

    return render_template(
        "dashboard.html",
        clientes=lista_clientes,
        productos=lista_productos
    )



if __name__ == "__main__":
    app.run(debug=True)