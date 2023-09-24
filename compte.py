from flask import redirect, render_template, request, Blueprint, session
import hashlib

bp_compte = Blueprint("compte", __name__)


def hacher_mot_de_passe(mdp):
    """Crypte le mot de passe"""
    return hashlib.sha512(mdp.encode()).hexdigest()


@bp_compte.route("/authentifier", methods=["GET", "POST"])
def connection():
    """permet de se connecter"""
    # GET
    if request.method == "GET":
        return render_template("compte/authentification.jinja")
    # POST
    mail = request.form.get("mail", default="")
    mdp = request.form.get("motdepasse", default="")
    return render_template("compte/authentification.jinja")

    # ici on va mettre  la connection a la bd et le tralala


def creer_session(identifiant):
    # cree la session

@bp_compte.route("/deconnecter")
def deconnection():
    return redirect("/", code=303)



