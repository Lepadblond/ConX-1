import re
from flask import redirect, render_template, request, Blueprint, session, abort
import hashlib
import app

bp_compte = Blueprint("compte", __name__)

# Expression régulière pour valider les adresses e-mail
regex_courriel = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


# Fonction pour hacher le mot de passe avec SHA-512
def hacher_mot_de_passe(mdp):
    return hashlib.sha512(mdp.encode()).hexdigest()


# Fonction pour créer une session utilisateur
def creer_session(user):
    if not user:
        return redirect("/authentifier", code=303)  # Redirige vers la page de connexion en cas d'échec
    else:
        session.permanent = True
        user["_id"] = str(user["_id"])
        session["user"] = user


# Route pour la déconnexion
@bp_compte.route("/deconnecter")
def deconnection():
    # ... Ajoutez ici la logique de déconnexion et de suppression de la session
    session.pop("user", None)

    return redirect("/", code=303)  # Redirige vers la page d'accueil après la déconnexion


# Route pour l'inscription
@bp_compte.route('/inscription', methods=['GET', 'POST'])
def inscription():
    """Inscription d'un utilisateur"""
    if request.method == 'GET':
        # Affiche la page de formulaire d'inscription lors de la requête GET
        return render_template('compte/inscription.jinja', message={})
    else:
        # Traite les données du formulaire d'inscription lors de la requête POST
        nom = request.form.get('nom')
        print(nom)
        prenom = request.form.get('prenom')
        print(prenom)
        mail = request.form.get('mail')
        mdp = request.form.get('mdp')
        mdp2 = request.form.get('mdp2')

        message = {}

        # Validation des données du formulaire (à décommenter et à compléter)
        if not nom or not mail or not mdp or not mdp2 or not prenom:
            message['nom'] = True,
            message['prenom'] = True,
            message['mail'] = True,
            message['mdp'] = True,
            message['mdp2'] = True,
        if mdp != mdp2:
            message['mdpMatch'] = True
        if not re.match(regex_courriel, mail):
            message['mail'] = True
        # Vérification de l'existence de l'adresse e-mail dans la base de données
        if app.mongo.db.users.find_one({"email": mail}) is not None:
            message['mail_existe'] = True
        print(message)
        if message != {}:
            # Si des erreurs sont présentes, affiche le formulaire avec les messages d'erreur
            return render_template('compte/inscription.jinja', message=message)
        else:
            # Hash du mot de passe (à décommenter)
            mdp = hacher_mot_de_passe(mdp)

            # Insertion de l'utilisateur dans la base de données
            app.mongo.db.users.insert_one({"nom": nom, "prenom": prenom, "email": mail, "password": mdp})
            user = app.mongo.db.users.find_one({"email": mail}, {"password": mdp})

            # # Création d'une session pour l'utilisateur inscrit
            creer_session(user)

            # Redirige vers la page d'accueil après l'inscription
            return redirect('/', code=303)
