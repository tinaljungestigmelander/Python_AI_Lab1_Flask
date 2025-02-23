from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from blueprints.db import get

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form.get("user_name")
        password = request.form.get("password")
        #password = request.form["password"]
        creds=get(user)
        if creds != None :
            if creds[1] == password:
                session["user"]=user
                flash("Loggin Successful")        
                return redirect(url_for("user_page.user"))
            else:
                flash("Invalid Password")
                return redirect(url_for("login.login"))
        else:
            # query={"user name" : user,"password" : password}
            # flash("User added")
            # add(query)            
            #users.insert_one({"user name" : user,"password" : password})
            session.pop('_flashes', None)
            flash("Redirecting to Sign Up")
            return render_template("create_user.html")          
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("home"))        
        return render_template("login.html")
    

    
# @login_bp.route("/get/<user>", methods=['GET','POST'])
# def get(user_name):
#     user = users.find_one({"user name": user_name})  # Hämta en användare

#     if user:
#         username = user["user name"]  # Hämta användarnamnet
#         password = user["password"]  # Hämta lösenordet
#         return [username,password]
#     else:
#         flash("User not found")
        

