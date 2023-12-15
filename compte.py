import re

from bson import ObjectId
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
        session["user"] = user
        user["_id"] = str(user["_id"])


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
        valeurChamp = {}
        # Affiche la page de formulaire d'inscription lors de la requête GET
        return render_template('compte/inscription.jinja', message={}, valeurChamp=valeurChamp)
    else:
        # Traite les données du formulaire d'inscription lors de la requête POST
        nom = request.form.get('nom')
        print(nom)
        prenom = request.form.get('prenom')
        print(prenom)
        mail = request.form.get('mail')
        mdp = request.form.get('mdp')
        mdp2 = request.form.get('mdp2')

        message = {
            'nom': False,
            'prenom': False,
            'mail': False,
            'mdp': False,
            'mdp2': False,
            'mdpMatch': False,
            'mail_existe': False
        }
        valeurChamp = {"nom": "", "prenom": "", "mail": ""}
        print(valeurChamp)

        # Validation des données du formulaire (à décommenter et à compléter)
        if not nom:
            message['nom'] = True
        else:
            valeurChamp['nom'] = nom

        if not prenom:
            message['prenom'] = True
        else:
            valeurChamp['prenom'] = prenom

        if not mail:
            message['mail'] = True
        else:
            valeurChamp['mail'] = mail

        if not mdp:
            message['mdp'] = True
        if not mdp2:
            message['mdp2'] = True

        if mdp != mdp2:
            message['mdpMatch'] = True
        if not re.match(regex_courriel, mail):
            message['mail'] = True
        # Vérification de l'existence de l'adresse e-mail dans la base de données
        if app.mongo.db.users.find_one({"email": mail}) is not None:
            message['mail_existe'] = True
        print(message)
        if any(message.values()):
            return render_template('compte/inscription.jinja', message=message, valeurChamp=valeurChamp)
        else:
            # Hash du mot de passe (à décommenter)
            mdp = hacher_mot_de_passe(mdp)

            # Insertion de l'utilisateur dans la base de données
            app.mongo.db.users.insert_one({"nom": nom, "prenom": prenom, "email": mail, "password": mdp})
            user = app.mongo.db.users.find_one({"email": mail}, {"password": mdp})

            # # Création d'une session pour l'utilisateur inscrit
            creer_session(user)
            object_id = str(user["_id"])
            print(object_id)

            # Redirige vers la page d'profil après l'inscription
            return redirect('/compte/profil/' + object_id, code=303)


@bp_compte.route('/profil/<string:id_utilisateur>', methods=['GET'])
def profil(id_utilisateur):
    """Afficher la page de profil"""
    if not session.get('user'):
        abort(401)
    user = session['user']

    if id_utilisateur != user['_id']:
        abort(403)

    object_id = ObjectId(id_utilisateur)
    user = app.mongo.db.users.find_one({"_id": object_id})
    message = {}

    # Retrieve the jobs added by the user
    listeemplois = list(app.mongo.db.emplois.find({"userId": id_utilisateur}))

    if not listeemplois:
        message["listeemplois"] = True

    return render_template('compte/profile.jinja', message=message, user=user, listeemplois=listeemplois)


@bp_compte.route('/profil/modifier/<string:id_utilisateur>', methods=['GET', 'POST'])
def modifiercompte(id_utilisateur):
    """Modifier le profil"""
    if not session.get('user'):
        abort(401)
    user = session['user']

    if id_utilisateur != user['_id']:
        abort(403)

    if request.method == 'GET':
        object_id = ObjectId(id_utilisateur)

        user = app.mongo.db.users.find_one({"_id": object_id})

        return render_template("compte/modifier.jinja", message={}, user=user)
    else:
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        # mail = request.form.get('mail')
        ville = request.form.get('ville')
        pays = request.form.get('pays')
        emploi = request.form.get('emploi')
        etude = request.form.get('etude')
        description = request.form.get('description')

        message = {}
        # Validation des données du formulaire
        if not nom or not prenom:
            message['nom'] = True,
            message['prenom'] = True,

        if len(nom) and len(prenom) < 1:
            message['nomOuPrenomTropCourt'] = True

        if message != {}:
            # Si des erreurs sont présentes, affiche le formulaire avec les messages d'erreur
            return render_template('compte/modifier.jinja', message=message, user=user)
        else:
            # Insertion de l'utilisateur dans la base de données
            object_id = ObjectId(id_utilisateur)
            app.mongo.db.users.update_one({"_id": object_id}, {
                "$set": {"nom": nom, "prenom": prenom, "ville": ville, "etude": etude, "pays": pays, "emploi": emploi,
                         "description": description}})
            user = app.mongo.db.users.find_one({"_id": object_id})
            print(user)
            # Redirige vers la page de profil après la modification
            return redirect('/compte/profil/' + id_utilisateur, code=303)
