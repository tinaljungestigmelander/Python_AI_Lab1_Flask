from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from blueprints.db import users, get


user_page_bp = Blueprint("user_page", __name__)

@user_page_bp.route("/user")
def user():
    if "user" in session: # If user is logged in username and password is shown on this page
        user=session["user"]
        usr=get(user)
        user_data={"Name":usr[0],"Password":usr[1]}                
        return render_template("user.html", user_name=user_data["Name"],password=user_data["Password"])
    else:
        flash("Please Login")
        return redirect(url_for("login.login")) # Redirect if user is not logged in

# Method to add a new user and save to db   
@user_page_bp.route("/add", methods=['POST'])
def add(): 
    user_name = request.form.get("user_name") # Get username and password from form
    password = request.form.get("password")  

    # Check that all fields are filled in
    if not user_name or not password:
        return "Both fields are required!", 400
    user=get(user_name)
    if user:
        flash("Username not available") # Check if username are already in db
        return redirect(url_for("login.login"))
    else: # Add user to db
        users.insert_one({"user name" : user_name,"password" : password})
        session.pop('_flashes', None) # Clean up flash() messages
        flash("User added")
        print(f"User {user_name} created with password {password}!")
        return redirect(url_for("login.login")) # Redirect to login

# Method to change password   
@user_page_bp.route("/update", methods=['POST'])
def update():
    usr=session["user"]
    user=get(usr)
    if user:
        username = user[0]      
    passwrd = request.form.get("password") # Get new password from form
    users.update_one(
    {"user name": username},  # Find row by user name
    {"$set": {"password": passwrd}}  # Update password
    )
    return redirect(url_for("user_page.user"))

# Method to delete user from db
@user_page_bp.route("/delete", methods=['POST'])
def delete():
    usr=session["user"] # Get user from session
    user=get(usr)
    if user:
        username = user[0]
        users.delete_one({"user name": username}) # Use user name to find row to delete
        flash("User deleted")
        session.pop("user", None) # Remove user from session
        return redirect(url_for("home"))
    else:
        flash("User not found")
        return redirect(url_for("user_page.user"))