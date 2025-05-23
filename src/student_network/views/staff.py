"""
Handles the view for staff administration tools and related functionality.
"""

from db import connect_to_db

import helpers.helper_connections as helper_connections
from flask import Blueprint, redirect, render_template, session

staff_blueprint = Blueprint(
    "staff", __name__, static_folder="static", template_folder="templates"
)


@staff_blueprint.route("/admin", methods=["GET", "POST"])
def show_staff_requests() -> object:
    """
    Displays requests to sign up as a staff member.

    Returns:
        The web page for handling administration.
    """
    if "admin" in session:
        if not session["admin"]:
            return render_template(
                "error.html",
                message=["Bạn không đăng nhập vào tài khoản quản trị"],
                requestCount=helper_connections.get_connection_request_count(),
            )
        with connect_to_db() as conn:
            # Loads the list of connection requests and their avatars.
            requests = []
            cur = conn.cursor()
            # Extracts incoming requests.
            cur.execute("SELECT username FROM accounts WHERE type='pending_staff';")
            conn.commit()
            row = cur.fetchall()
            if len(row) > 0:
                for elem in row:
                    requests.append(elem[0])

            return render_template(
                "admin.html",
                requests=requests,
                requestCount=helper_connections.get_connection_request_count(),
            )
    else:
        return render_template(
            "error.html",
            message=["Bạn không đăng nhập vào tài khoản quản trị"],
            requestCount=helper_connections.get_connection_request_count(),
        )


@staff_blueprint.route("/accept_staff/<username>", methods=["GET", "POST"])
def accept_staff(username: str):
    """
    Accepts user as a staff member.

    Args:
        username: The user to accept as a staff member.

    Returns:
        Redirection to the administration page.
    """
    with connect_to_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE accounts SET type=%s WHERE username=%s ;", ("staff", username)
        )
    return redirect("/admin")


@staff_blueprint.route("/reject_staff/<username>", methods=["GET", "POST"])
def reject_staff(username: str):
    """
    Rejects user as staff member.

    Args:
        username: The user to reject as a staff member.

    Returns:
        Redirection to the administration page.
    """
    with connect_to_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE accounts SET type=%s WHERE username=%s ;", ("student", username)
        )
    return redirect("/admin")
