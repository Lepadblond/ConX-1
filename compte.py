import re

from flask import redirect, render_template, request, Blueprint, session
import hashlib

bp_compte = Blueprint("compte", __name__)

regex_courriel = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


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
    """Crée une session"""

    return redirect("/", code=303)


@bp_compte.route("/deconnecter")
def deconnection():
    return redirect("/", code=303)


@bp_compte.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'GET':
        return render_template('compte/inscription.jinja', message={})
    else:
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        mail = request.form.get('mail')
        mdp = request.form.get('mdp')
        mdp2 = request.form.get('mdp2')
        message = {}
        if not nom or not mail or not mdp or not mdp2 or not prenom:
            message['vide'] = 'Veuillez remplir tous les champs'
        if mdp != mdp2:
            message['mdp'] = 'Les mots de passe ne correspondent pas'
        if not re.match(regex_courriel, mail):
            message['mail'] = 'Adresse mail invalide'

        if message != {}:
            return render_template('compte/inscription.jinja', message=message)
        else:
            mdp = hacher_mot_de_passe(mdp)
            # with bd.creer_connexion() as conn:
            #     if bd.email_exists(conn, mail):
            #         message['mail'] = 'Adresse mail déjà utilisée'
            #         return render_template('inscription.html', message=message)
            #     else:
            #         bd.creer_compte(conn, nom, mail, mdp)
            #         id_user = bd.get_id(conn, mdp, mail)
            #       creer_session(id_user["id_utilisateur"])
        return redirect('/compte/authentifier', code=303)
