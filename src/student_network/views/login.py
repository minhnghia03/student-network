"""
Handles the view for the login system and related functionality.
"""

from db import connect_to_db
from datetime import date
from string import capwords

import bcrypt
import helpers.helper_connections as helper_connections
import helpers.helper_general as helper_general
import helpers.helper_login as helper_login
from flask import Blueprint, redirect, render_template, request, session
import helpers.helper_oauth as helper_oauth

login_blueprint = Blueprint(
    "login", __name__, static_folder="static", template_folder="templates"
)


@login_blueprint.route("/", methods=["GET"])
def index_page() -> object:
    """
    Renders the feed page if the user is logged in.

    Returns:
        The web page for user login.
    """
    if "username" in session:
        return redirect("/profile")
    else:
        session["prev-page"] = request.url
        return render_template("home_page.html")


@login_blueprint.route("/login", methods=["GET"])
def login_page() -> object:
    """
    Renders the login page.

    Returns:
        The web page for user login.
    """
    # get the code
    if request.args.get("code"):
        try:
            helper_oauth.oauth_login(request.args.get("code"), session)
        except Exception as e:
            print(e)
            pass
    errors = []
    if "username" in session:
        return redirect("/profile")
    else:
        if "error" in session:
            errors = session["error"]
        session["prev-page"] = request.url
        # Clear error session variables.
        session.pop("error", None)
        return render_template("login.html", errors=errors)


@login_blueprint.route("/terms", methods=["GET", "POST"])
def terms_page() -> object:
    """
    Renders the terms and conditions page.

    Returns:
        The web page for T&Cs, or redirection back to register page.
    """
    if request.method == "GET":
        session["prev-page"] = request.url
        return render_template(
            "terms.html", requestCount=helper_connections.get_connection_request_count()
        )
    else:
        return redirect("/register")


@login_blueprint.route("/privacy_policy", methods=["GET", "POST"])
def privacy_policy_page() -> object:
    """
    Renders the privacy policy page.

    Returns:
        The web page for the privacy policy, or redirection back to T&Cs.
    """
    if request.method == "GET":
        session["prev-page"] = request.url
        return render_template(
            "privacy_policy.html",
            requestCount=helper_connections.get_connection_request_count(),
        )
    else:
        return redirect("/terms")


@login_blueprint.route("/login", methods=["POST"])
def login_submit() -> object:
    """
    Validates the user's login details.

    Returns:
         Redirection depending on whether login was successful or not.
    """
    username = request.form["username_input"].lower()
    password = request.form["psw_input"].encode("utf-8")

    with connect_to_db() as conn:
        cur = conn.cursor()
        # Gets user from database using username.
        cur.execute(
            "SELECT password, type FROM accounts WHERE username=%s and moodle_id is NULL;",
            (username,),
        )
        conn.commit()
        row = cur.fetchone()
        if row:
            hashed_password = row[0]
            account_type = row[1]
        else:
            session["error"] = ["login"]
            return redirect("/login")
        if hashed_password:
            if bcrypt.checkpw(password, hashed_password.encode("utf-8")):
                session["username"] = username
                session["prev-page"] = request.url
                if account_type == "admin":
                    session["admin"] = True
                    return redirect("/admin")
                else:
                    session["admin"] = False
                    return redirect("/profile")
            else:
                session["error"] = ["login"]
                return redirect("/login")
        else:
            session["error"] = ["login"]
            return redirect("/login")


@login_blueprint.route("/register", methods=["GET"])
def register_page() -> object:
    """
    Renders the user registration page.

    Returns:
        The web page for user registration.
    """
    notifications = []
    errors = ""
    if "username" in session:
        return redirect("/profile")
    else:
        if "notifications" in session:
            notifications = session["notifications"]
        if "error" in session:
            errors = session["error"]
        session.pop("error", None)
        session.pop("notifications", None)
        session["prev-page"] = request.url

        if "register_details" in session:
            details = session["register_details"]
        else:
            details = ["", "", ""]
        return render_template(
            "register.html",
            notifications=notifications,
            errors=errors,
            details=details,
            requestCount=helper_connections.get_connection_request_count(),
        )


@login_blueprint.route("/register", methods=["POST"])
def register_submit() -> object:
    """
    Registers an account using the user's input from the registration form.

    Returns:
        The updated web page based on whether the details provided were valid.
    """
    # Obtains user input from the account registration form.
    username = request.form["username_input"].lower()
    full_name = capwords(request.form["fullname_input"])
    password = request.form["psw_input"]
    password_confirm = request.form["psw_input_check"]
    email = request.form["email_input"]
    terms = request.form.get("terms")
    account = request.form.get("optradio")

    # Connects to the database to perform validation.
    with connect_to_db() as conn:
        cur = conn.cursor()
        valid, message = helper_login.validate_registration(
            cur, username, full_name, password, password_confirm, email, terms
        )
        # Registers the user if the details are valid.
        if valid is True:
            hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            cur.execute(
                "INSERT INTO accounts (username, password, email, type) "
                "VALUES (%s, %s, %s, %s);",
                (
                    username,
                    hash_password,
                    email,
                    account,
                ),
            )
            cur.execute(
                "INSERT INTO user_profile (username, name, bio, gender, "
                "birthday, profilepicture) "
                "VALUES (%s, %s, %s, %s, %s, %s);",
                (
                    username,
                    full_name,
                    "Thay đổi bio của bạn trong cài đặt.",
                    "Male",
                    date.today(),
                    "/static/images/default-pfp.jpg",
                ),
            )
            helper_general.check_level_exists(username, conn)
            conn.commit()

            session["notifications"] = ["register"]
            session["username"] = username
            return redirect("/register")
        # Displays error message(s) stating why their details are invalid.
        else:
            details = [username, full_name, email]
            session["register_details"] = details

            session["error"] = message
            return redirect("/register")


@login_blueprint.route("/logout", methods=["GET"])
def logout() -> object:
    """
    Clears the user's session if they are logged in.

    Returns:
        The web page for logging in if the user logged out of an account.
    """
    if "username" in session:
        session.clear()
        session["prev-page"] = request.url
        return redirect("/login")
    return redirect("/")
