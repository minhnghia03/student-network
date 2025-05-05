import requests

from db import connect_to_db
from flask import redirect
from datetime import date
import helpers.helper_general as helper_general
import os


def oauth_login(code: str, session: dict) -> str:
    response = requests.post(
        os.getenv("OAUTH_TOKEN_URL"),
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": os.getenv("OAUTH_CLIENT_ID"),
            "client_secret": os.getenv("CLIENT_SECRET"),
            "scope": "user_info",
        },
    )
    if response.status_code != 200:
        print(response.json())
        raise Exception("Failed to get access token")
    access_token = response.json()["access_token"]
    response = requests.post(
        os.getenv("OAUTH_USER_INFO_URL"),
        data={"access_token": access_token},
    )
    if response.status_code != 200:
        print(response.json())
        raise Exception("Failed to get user info")
    user_info = response.json()
    with connect_to_db() as conn:
        cur = conn.cursor()
        moodle_id = user_info["id"]
        cur.execute(
            "SELECT username, type FROM accounts WHERE moodle_id=%s;", (moodle_id,)
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

            with connect_to_db() as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO accounts (username, password, email, type, moodle_id) "
                    "VALUES (%s, %s, %s, %s, %s);",
                    (
                        username,
                        "unhashed",
                        email,
                        account,
                        moodle_id,
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
