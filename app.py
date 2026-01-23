from flask import Flask, render_template, request, redirect, url_for, session
from pathlib import Path
import POKEMONDECKBUILDER  # type: ignore

projectRoot = Path(__file__).parent
storageDir = projectRoot / "PokemonStorage"
storageDir.mkdir(exist_ok=True)
jsonFile = storageDir / "cards.json"

preCards = (POKEMONDECKBUILDER.loadCards(jsonFile))
totalCards = []
# for key in preCards:
#     totalCards += preCards[key]


# MY APP
app = Flask(__name__)
app.secret_key = "123123"


@app.route("/")
def index():
    if "storageOption" not in session:
        session["storageOption"] = "Main Storage"
    preCards = (POKEMONDECKBUILDER.loadCards(jsonFile))
    cards = preCards[session["storageOption"]]
    linkList = POKEMONDECKBUILDER.listopenurl(cards)
    return render_template("index.html", cardData=cards, linkData=linkList, activeStorage=session["storageOption"], keyData=preCards)


@app.route('/submit', methods=['POST'])
def submit():
    val1 = request.form.get('cardName')
    val2 = request.form.get('cardSet')
    val3 = request.form.get('cardNumber')
    val4 = request.form.get('amount')
    vals = [val1, val2, val3, val4]
    POKEMONDECKBUILDER.inputcards(session["storageOption"], jsonFile, vals)
    return redirect(url_for('index'))


@app.route('/submitStorage', methods=['POST'])
def submitStorage():
    val = request.form.get('storage')
    session["storageOption"] = val
    print(session["storageOption"])
    return redirect(url_for('index'))


@app.route('/imageAction', methods=["POST"])
def imageAction():
    action = request.form["action"]
    vals = [
        request.form["cardName"],
        request.form["cardSet"],
        int(request.form["cardNumber"])
    ]
    if action == "add":
        POKEMONDECKBUILDER.addOrRemove(
            session["storageOption"], jsonFile, vals, 1)
    else:
        POKEMONDECKBUILDER.addOrRemove(
            session["storageOption"], jsonFile, vals, 0)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)


#####
# LOOP THROUGH THE KEYS OF THE JSON FILE AND PASS IT THROUGH INDEX
# {% for key in dict %}
#   {% for card in cardData[key] %}

# when hovering over particular image grey out and show card amount
