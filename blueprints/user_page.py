from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from blueprints.db import users, get


user_page_bp = Blueprint("user_page", __name__)

@user_page_bp.route("/user")
def user():
    if "user" in session:
        user=session["user"]
        usr=get(user)
        user_data={"Name":usr[0],"Password":usr[1]}                
        return render_template("user.html", user_name=user_data["Name"],password=user_data["Password"])
    else:
        flash("Please Login")
        return redirect(url_for("login.login"))
    
@user_page_bp.route("/add", methods=['POST'])
def add():
        #users.insert_one(query)
    user_name = request.form.get("user_name")
    password = request.form.get("password")  

    # Kontrollera att båda fälten är ifyllda
    if not user_name or not password:
        return "Both fields are required!", 400
    user=get(user_name)
    if user:
        flash("Username not available")
        return redirect(url_for("login.login"))
    else:
        users.insert_one({"user name" : user_name,"password" : password})
        session.pop('_flashes', None)
        flash("User added")
        print(f"User {user_name} created with password {password}!")
        return redirect(url_for("login.login"))
    
@user_page_bp.route("/update", methods=['POST'])
def update():
    usr=session["user"]
    user=get(usr)
    if user:
        username = user[0]  # Hämta användarnamnet    
    passwrd = request.form.get("password") 
    users.update_one(
    {"user name": username},  # Sök på användarnamn
    {"$set": {"password": passwrd}}  # Uppdatera lösenordet
    )
    return redirect(url_for("user_page.user"))

@user_page_bp.route("/delete", methods=['POST'])
def delete():
    usr=session["user"]
    user=get(usr)
    if user:
        username = user[0]
        users.delete_one({"user name": username})
        flash("User deleted")
        session.pop("user", None)
        return redirect(url_for("home"))
    else:
        flash("User not found")
        return redirect(url_for("user_page.user"))