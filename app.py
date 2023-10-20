from flask import Flask, render_template, request, redirect, session
from flask_pymongo import PyMongo
import os
from compte import bp_compte
import hashlib

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv('CONNEXION_BD')

app.register_blueprint(bp_compte, url_prefix="/compte")

app.secret_key = "e21f73185e51e634aa9ef799c70878d366a55b7fd626981f271b66b10ac65c84"
mongo = PyMongo(app)


@app.route("/",methods=["GET", "POST"])
def index():
    """Afficher la page index"""
    message = {}
    if request.method == "GET":

        # Affiche la page de formulaire de connexion lors de la requête GET
        return render_template("index.jinja", message={})
    else:
        # Traite les données du formulaire de connexion lors de la requête POST
        mail = request.form.get("mail", default="")
        mdp = request.form.get("mdp", default="")

        if not mail:
            message["mail"] = True
        if not mdp:
            message["mdp"] = True
        if message:
            return render_template("index.jinja", message=message, mail=mail)
        mdp = hacher_mot_de_passe(mdp)
        user = mongo.db.users.find_one({"email": mail}, {"password": mdp})
        if user is not None:
            creer_session(user)

    return redirect("/")


def hacher_mot_de_passe(mdp):
    return hashlib.sha512(mdp.encode()).hexdigest()


def creer_session(user):
    if not user:
        return redirect("/", code=303)  # Redirige vers la page de connexion en cas d'échec
    else:
        session.permanent = True
        user["_id"] = str(user["_id"])
        session["user"] = user
