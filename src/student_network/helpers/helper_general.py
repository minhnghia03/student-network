"""
Performs checks and actions to help the general system work effectively.
"""

from db import connect_to_db
from datetime import datetime
from math import floor
from typing import Tuple

import helpers.helper_profile as helper_profile
from flask import session


def is_allowed_photo_file(file_name) -> bool:
    """
    Checks if the file is an allowed type.

    Args:
        file_name: The name of the file uploaded by the user.

    Returns:
        Whether the file is allowed or not (True/False).
    """
    return "." in file_name and file_name.rsplit(".", 1)[1].lower() in {
        "png",
        "jpg",
        "jpeg",
        "gif",
    }


def display_short_notification_age(seconds):
    prefixes = ["y", "mo", "d", "h", "m", "s"]
    values = [3600 * 24 * 365, 3600 * 31 * 24, 3600 * 24, 3600, 60, 1]

    for i in range(len(prefixes)):
        if seconds >= values[i]:
            return str(floor(seconds / values[i])) + prefixes[i]

    return "Just Now"


def get_all_connections(username: str) -> list:
    """
    Gets a list of all usernames that are connected to the logged in user.

    Returns:
        A list of all usernames that are connected to the logged in user.
    """
    with connect_to_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT user2 FROM connection "
            "WHERE user1=%s AND connection_type='connected' UNION ALL "
            "SELECT user1 FROM connection "
            "WHERE user2=%s AND connection_type='connected'",
            (username, username),
        )
        connections = cur.fetchall()

        return connections


def get_all_usernames() -> list:
    """
    Gets a list of all usernames that are registered.

    Returns:
        A list of all usernames that have been registered.
    """
    with connect_to_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT username FROM accounts")

        row = cur.fetchall()

        return row


def get_notifications():
    with connect_to_db() as conn:
        cur = conn.cursor()

        cur.execute(
            "SELECT body, date, url FROM notification WHERE username=%s ORDER "
            "BY date DESC",
            (session["username"],),
        )

        row = cur.fetchall()

        notification_metadata = list(
            map(
                lambda x: (
                    x[0],
                    display_short_notification_age(
                        (datetime.now() - x[1]).total_seconds()
                    ),
                    x[2],
                ),
                row,
            )
        )

        return notification_metadata


def check_level_exists(username: str, conn):
    """
    Checks that a user has a record in the database for their level.

    Args:
        username: The username of the user to check.
        conn: The connection to the database.
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_level WHERE username=%s;", (username,))
    if cur.fetchone() is None:
        cur.execute(
            "INSERT INTO user_level (username, experience) VALUES (%s, %s);",
            (username, 0),
        )
        conn.commit()


def get_messages(username: str):
    """
    Get messages between logged in user and each user with chats

    Args:
        username: user to get messages of
    """
    with connect_to_db() as conn:
        cur = conn.cursor()

        cur.execute(
            "SELECT message, sender, date FROM private_messages WHERE (sender=%s AND receiver=%s) ",
            (session["username"], username),
        )
        row = cur.fetchall()

        cur.execute(
            "SELECT message, sender, date FROM private_messages WHERE (sender=%s AND receiver=%s) ",
            (username, session["username"]),
        )
        row += cur.fetchall()

        if row == []:
            return [[""], "", ""]

        row.sort(key=lambda x: x[2], reverse=True)

        return [row, "", ""]


def recent_message(date: str) -> Tuple[str, int]:
    """
    Get time since the most recent message

    Args:
        date: datetime of message

    Returns:
        [type]: [description]
    """
    seconds = (datetime.now() - date).total_seconds()
    elapsed = display_short_notification_age(seconds)

    return (elapsed, seconds)


def get_rooms():
    """
    Get chat rooms for user

    Returns:
        chat rooms of user
    """
    chat_rooms = get_all_connections(session["username"])
    chat_rooms = list(
        map(lambda x: (x[0], helper_profile.get_profile_picture(x[0])), chat_rooms)
    )

    chat_rooms = [list(x) for x in chat_rooms]

    for i, room in enumerate(chat_rooms):
        message = get_messages(room[0])
        if message[0][0] != "":
            message[1], message[2] = recent_message(message[0][0][2])
        chat_rooms[i].append(message)

    actives = [x for x in chat_rooms if x[2][2] != ""]
    inactives = [x for x in chat_rooms if x[2][2] == ""]
    actives.sort(key=lambda x: x[2][2])
    chat_rooms = actives + inactives

    return chat_rooms


def one_exp(cur, username: str):
    """
    Awards 1 exp point

    Args:
        username: user to award exp to
    """
    cur.execute(
        "UPDATE user_level SET experience = experience + 1 WHERE username=%s;",
        (username,),
    )


def get_exp(username: str):
    """
    Get current exp of given user

    Args:
        username: user to find exp value of

    Returns:
        exp of user
    """
    with connect_to_db() as conn:
        cur = conn.cursor()
        check_level_exists(username, conn)
        # Get user experience
        cur.execute("SELECT experience FROM user_level WHERE username=%s;", (username,))
        row = cur.fetchone()

        return int(row[0])


def new_notification(body, url):
    now = datetime.now()

    with connect_to_db() as conn:
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO notification (username, body, date, url) VALUES (%s, %s, %s, %s);",
            (session["username"], body, now.strftime("%Y-%m-%d %H:%M:%S"), url),
        )

        conn.commit()


def new_notification_username(username, body, url):
    now = datetime.now()

    with connect_to_db() as conn:
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO notification (username, body, date, url) VALUES (%s, %s, %s, %s);",
            (username, body, now.strftime("%Y-%m-%d %H:%M:%S"), url),
        )

        conn.commit()
