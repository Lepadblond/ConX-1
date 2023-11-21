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
        print(emploi)

        # je retourne la page de l'emploi avec les données
        return render_template("emploi/emploidetail.jinja", emploi=emploi)

# Route pour ajouter un emploi
