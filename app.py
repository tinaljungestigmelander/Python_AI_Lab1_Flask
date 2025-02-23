import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, session, flash
from datetime import timedelta
from blueprints.login import login_bp
from blueprints.user_page import user_page_bp
from blueprints.db import db_bp

app = Flask(__name__)
load_dotenv()
app.secret_key=os.getenv("SECRET_KEY")
app.permanent_session_lifetime = timedelta(minutes=5)

app.register_blueprint(login_bp, url_prefix="/login")
app.register_blueprint(user_page_bp, url_prefix="/user_page")
app.register_blueprint(db_bp, url_prefix="/db")


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")
    
@app.route('/blackjack')
def blackjack():
    return render_template("blackjack.html")        

@app.route("/logout")
def logout():
    if not "user" in session:
        flash("Already logged out")
        return redirect(url_for("login.login"))
    else:
        flash("You have been logged out!", "info")
        session.pop("user", None)   
        return redirect(url_for("login.login"))


if __name__ == "__main__":
    app.run(debug=True)
