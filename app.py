from flask import Flask, render_template
from flask_pymongo import PyMongo
from dotenv import dotenv_values

config = dotenv_values(".env")


app = Flask(__name__)
app.config["MONGO_URI"] = config['CONNEXION_BD']
mongo = PyMongo(app)

produits = mongo.db.products.find()


@app.route("/")
def index():
    return render_template("base.jinja")