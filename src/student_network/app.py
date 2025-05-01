"""
A student network application which is presented as a web application using
the Flask module. Students each have their own profile page, and they can post
on their feed.
"""

from datetime import datetime

import views.achievements as achievements
import views.chat as chat
import views.connections as connections
import views.flashcards as flashcards
import views.login as login
import views.posts as posts
import views.profile as profile
import views.quizzes as quizzes
import views.staff as staff
from flask import Flask, request, session
from flask_socketio import SocketIO
from db import connect_to_db


app = Flask(__name__)
socketio = SocketIO(app)
app.register_blueprint(achievements.achievements_blueprint, url_prefix="")
app.register_blueprint(chat.chat_blueprint, url_prefix="")
app.register_blueprint(connections.connections_blueprint, url_prefix="")
app.register_blueprint(login.login_blueprint, url_prefix="")
app.register_blueprint(posts.posts_blueprint, url_prefix="")
app.register_blueprint(profile.profile_blueprint, url_prefix="")
app.register_blueprint(quizzes.quizzes_blueprint, url_prefix="")
app.register_blueprint(flashcards.flashcards_blueprint, url_prefix="")
app.register_blueprint(staff.staff_blueprint, url_prefix="")
app.secret_key = '\xfd{H\xe5 <\x95\xf9\xe3\x96.5\xd1\x01O <!\xd5"xa2\xa0\x9fR\xa1\xa8'
app.url_map.strict_slashes = False
users = {}


@socketio.on("username", namespace="/private")
def receive_username(username):
    users[username] = request.sid


@socketio.on("private_message", namespace="/private")
def private_message(payload):
    with connect_to_db() as conn:
        cur = conn.cursor()

        now = datetime.now()

        cur.execute(
            "INSERT INTO private_messages "
            "(sender, receiver, message, date) VALUES (%s, %s, %s, %s);",
            (
                session["username"],
                payload["username"],
                payload["message"],
                now.strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )

        conn.commit()

    if payload["username"] in users:
        recipient_session_id = users[payload["username"]]

        socketio.emit(
            "new_private_message",
            payload,
            room=recipient_session_id,
            namespace="/private",
        )
    # user is not online at the moment
    else:
        pass


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
