import requests

import sqlite3
from flask import redirect
from datetime import date
import helpers.helper_general as helper_general


def oauth_login(code: str, session: dict) -> str:
    response = requests.post(
        "http://localhost:8080/local/oauth/token.php",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": "hsa-connect",
            "client_secret": "39086837c1bbba8a8598f01a8cad5c698325a63edbfd0b9d",
            "scope": "user_info",
        },
    )
    if response.status_code != 200:
        print(response.json())
        raise Exception("Failed to get access token")
    access_token = response.json()["access_token"]
    response = requests.post(
        "http://localhost:8080/local/oauth/user_info.php",
        data={"access_token": access_token},
    )
    if response.status_code != 200:
        print(response.json())
        raise Exception("Failed to get user info")
    user_info = response.json()
    with sqlite3.connect("db.sqlite3") as conn:
        cur = conn.cursor()
        moodle_id = user_info["id"]
        cur.execute(
            "SELECT username, type FROM ACCOUNTS WHERE moodle_id=?;", (moodle_id,)
        )
        conn.commit()
        row = cur.fetchone()
        if row:
            username = row[0]
            account_type = row[1]
            session["username"] = username
            if account_type == "admin":
                session["admin"] = True
                return redirect("/admin")
            else:
                session["admin"] = False
                return redirect("/profile")
        else:
            print("user_info", user_info)
            username = user_info["username"]
            full_name = user_info["firstname"] + " " + user_info["lastname"]
            account = "student"
            email = user_info["email"]

            with sqlite3.connect("db.sqlite3") as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO Accounts (username, password, email, type, moodle_id) "
                    "VALUES (?, ?, ?, ?, ?);",
                    (
                        username,
                        "unhashed",
                        email,
                        account,
                        moodle_id,
                    ),
                )

                cur.execute(
                    "INSERT INTO UserProfile (username, name, bio, gender, "
                    "birthday, profilepicture) "
                    "VALUES (?, ?, ?, ?, ?, ?);",
                    (
                        username,
                        full_name,
                        "Change your bio in the settings.",
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
