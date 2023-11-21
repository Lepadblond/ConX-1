import re

from bson import ObjectId
from flask import redirect, render_template, request, Blueprint, session, abort
import hashlib
import app

bp_emploi = Blueprint("emploi", __name__)


# route pour afficher les emplois
@bp_emploi.route("/emplois")
def afficherlesemplois():
    """Afficher les emplois"""

    # je verifie si l'utilisateur est connecté sinon je redirige vers la page de connexion /
    if not session.get("user"):
        return redirect("/", code=303)
    else:
        # je recupere les emplois dans la base de données
        emplois = app.mongo.db.emplois.find()
        # je retourne la page des emplois avec les données
        return render_template("emploi/emplois.jinja", emplois=emplois)
