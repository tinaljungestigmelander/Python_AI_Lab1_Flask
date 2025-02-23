from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from blueprints.db import get

login_bp = Blueprint("login", __name__)

# Method for login
@login_bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form.get("user_name") # Gets user name  and password from form
        password = request.form.get("password")
        creds=get(user) # Calls get() method to check if user is in db
        if creds != None :
            if creds[1] == password: # If user in db, check if password is correct
                session["user"]=user # If ok, user is saved in session
                flash("Loggin Successful")        
                return redirect(url_for("user_page.user")) # Redirect to user page
            else:
                flash("Invalid Password")
                return redirect(url_for("login.login")) # Sends user back to login if password is wrong
        else:
            session.pop('_flashes', None)
            flash("Redirecting to Sign Up") # If user not in db, redirecting to page for creating new user
            return render_template("create_user.html")          
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("home"))        
        return render_template("login.html")
    

    

        

