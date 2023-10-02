from dotenv import dotenv_values
from flask import Flask, render_template
from flask_pymongo import PyMongo
import os
from compte import bp_compte

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv('CONNEXION_BD')
mongo = PyMongo(app)

app.register_blueprint(bp_compte, url_prefix="/compte")

app.secret_key = "e21f73185e51e634aa9ef799c70878d366a55b7fd626981f271b66b10ac65c84"


@app.route("/")
def index():
    return render_template("base.jinja")
