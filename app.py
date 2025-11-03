from flask import Flask, render_template, request, redirect, url_for, jsonify
import json, os
from datetime import datetime

app = Flask(__name__)

# Emplacement du fichier où seront enregistrées les légendes
LEGENDS_FILE = os.path.join(os.path.dirname(__file__), "legends.json")

def ensure_legends_file():
    """Crée le fichier legends.json s’il n’existe pas."""
    if not os.path.exists(LEGENDS_FILE):
        with open(LEGENDS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

def read_legends():
    """Lit le contenu du fichier legends.json."""
    ensure_legends_file()
    with open(LEGENDS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def write_legends(data):
    """Écrit la liste de légendes dans le fichier legends.json."""
    ensure_legends_file()
    with open(LEGENDS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
@app.route("/accueil")
def accueil():
    return render_template("accueil.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/don", methods=["GET", "POST"])
def don():
    if request.method == "POST":
        montant = request.form.get("montant", "").strip()
        business = "anonymous-donations"
        paypal_url = f"https://www.paypal.com/donate/?business={business}&currency_code=EUR"
        if montant:
            paypal_url += f"&amount={montant}"
        return redirect(paypal_url)
    return render_template("don.html")

@app.route("/legendes", methods=["GET", "POST"])
def legendes():
    """Affiche et enregistre les légendes envoyées par les utilisateurs."""
    if request.method == "POST":
        titre = request.form.get("titre", "").strip()
        auteur = request.form.get("auteur", "").strip() or "Anonyme"
        texte = request.form.get("texte", "").strip()
        if titre and texte:
            legends = read_legends()
            legends.insert(0, {
                "titre": titre,
                "auteur": auteur,
                "texte": texte,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            write_legends(legends)
        return redirect(url_for("legendes"))
    legends = read_legends()
    return render_template("legendes.html", legends=legends)

@app.route("/jeddi")
def jeddi():
    return render_template("jeddi.html")

# Point d’entrée principal
if __name__ == "__main__":
    ensure_legends_file()
    from os import environ
    app.run(host="0.0.0.0", port=int(environ.get("PORT", 5000)), debug=True)
