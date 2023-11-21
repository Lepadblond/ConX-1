import re

from bson import ObjectId
from flask import redirect, render_template, request, Blueprint, session, abort
import app

bp_emploi = Blueprint("emploi", __name__)


# route pour afficher les emplois
@bp_emploi.route("/")
def afficherlesemplois():
    """Afficher les emplois"""

    # je verifie si l'utilisateur est connecté sinon je redirige vers la page de connexion /
    if not session.get("user"):
        return redirect("/", code=303)
    else:
        # je recupere les emplois dans la base de données
        emplois = app.mongo.db.emplois.find()
        listeemplois = list(emplois)
        print(listeemplois)
        # je retourne la page des emplois avec les données
        return render_template("emploi/emploi.jinja", listeemplois=listeemplois)


# route pour afficher un emploi
@bp_emploi.route("détail/<string:id_emploi>")
def afficherlemploi(id_emploi):
    """Afficher un emploi"""

    # je verifie si l'utilisateur est connecté sinon je redirige vers la page de connexion /
    if not session.get("user"):
        return redirect("/", code=303)
    else:
        # je recupere l'emploi dans la base de données
        object_id = ObjectId(id_emploi)
        emploi = app.mongo.db.emplois.find_one({"_id": object_id})

        # je retourne la page de l'emploi avec les données
        return render_template("emploi/emploidetail.jinja", emploi=emploi)


# Route pour ajouter un emploi
@bp_emploi.route("/ajouter", methods=["GET", "POST"])
def ajouteremploi():
    """Ajouter un emploi"""

    # je verifie si l'utilisateur est connecté sinon je redirige vers la page de connexion /
    if not session.get("user"):
        return redirect("/", code=303)
    else:
        if request.method == "GET":
            # je retourne la page du formulaire d'ajout d'emploi
            return render_template("emploi/ajouteremploi.jinja", message={})
        else:
            entreprise = {"nom": "", "adresse": "", "siteWeb": ""}

            # je recupere les données du formulaire
            titre = request.form.get("titre", default="")
            description = request.form.get("description", default="")
            entreprise.nom = request.form.get("entrepriseNom", default="")
            entreprise.adresse = request.form.get("entrepriseAdresse", default="")
            entreprise.siteWeb = request.form.get("entrepriseSiteWeb", default="")
            lieu = request.form.get("lieu", default="")
            salaire = request.form.get("salaire", type=int, default=0)
            user = session.get("user")
            id_user = user["_id"]
            print(id_user)
            message = {}
            # je verifie si les champs sont vides
            if not titre or not description or not entreprise.nom or not entreprise.adresse or not entreprise.siteWeb or not lieu or not salaire:
                message['titre'] = True,
                message['description'] = True,
                message['entrepriseNom'] = True,
                message['entrepriseAdresse'] = True,
                message['entrepriseSiteWeb'] = True,
                message['lieu'] = True,
                message['salaire'] = True,
                

                return render_template("emploi/ajouteremploi.jinja", message=message)
            else:
                # j insere l'emploi dans la base de données

                resultat = app.mongo.db.emplois.insert_one({
                    "titre": titre,
                    "description": description,
                    "entreprise": entreprise,
                    "lieu": lieu,
                    "salaire": salaire,
                    "userId": id_user
                })

                resultatid = resultat.inserted_id
                object_id = ObjectId(resultatid)
                emploi = app.mongo.db.emplois.find_one({"_id": object_id})
                # je redirige vers la page details des emplois
                return redirect("/emploi/détail/" + str(emploi["_id"]), code=303)
