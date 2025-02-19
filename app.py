from flask import Flask, render_template, redirect, url_for, request, session, flash

app = Flask(__name__)
app.secret_key = "hello"

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("home"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))
        
        return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return redirect(url_for("home"))
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    flash("You have been logged out!", "info")
    session.pop("user", None)   
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
