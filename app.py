import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, session, flash
from datetime import timedelta
from blueprints.login import login_bp # Imports blueprints
from blueprints.user_page import user_page_bp
from blueprints.db import db_bp
from blueprints.black_jack import black_jack_bp

app = Flask(__name__)
load_dotenv()
app.secret_key=os.getenv("SECRET_KEY")
app.permanent_session_lifetime = timedelta(minutes=5) # Sets how long session data is saved


app.register_blueprint(login_bp, url_prefix="/login") # Activate my blueprints
app.register_blueprint(user_page_bp, url_prefix="/user_page")
app.register_blueprint(db_bp, url_prefix="/db")
app.register_blueprint(black_jack_bp, url_prefix="/black_jack")


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")
    
@app.route('/blackjack', methods=['GET','POST'])
def blackjack():
    if "user" in session: # Check if user is logged in before redirecting to game
        return redirect(url_for("black_jack.set_up"))
    else:
        return redirect(url_for("login.login"))        

# Logout method
@app.route("/logout")
def logout():
    if not "user" in session: # Check if user is logged in
        flash("Already logged out")
        return redirect(url_for("login.login"))
    else:
        flash("You have been logged out!", "info")
        session.pop("user", None) # Remove user from session when logged out   
        return redirect(url_for("login.login"))

# Code from ChatGPT
# Mappa kortens namn till Unicode-symboler
CARD_UNICODE = {
    "hearts": "♥️",
    "diamonds": "♦️",
    "clubs": "♣️",
    "spades": "♠️"
}

def get_unicode_card(card):
    """Konvertera kort till Unicode-symboler, t.ex. 'hearts 10' → '♥️10'"""
    suit, value = card.split()  # Dela upp i färg och värde
    return f"{CARD_UNICODE.get(suit, suit)}{value}"

# Code from ChatGPT
app.jinja_env.filters["unicode_card"] = get_unicode_card
print(get_unicode_card("hearts 10"))  # Borde ge: ♥️10
print(get_unicode_card("spades 5"))  # Borde ge: ♠️5

if __name__ == "__main__":
    app.run(debug=True)
