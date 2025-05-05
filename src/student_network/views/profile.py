"""
Handles the view for user profiles and related functionality.
"""

from db import connect_to_db
from datetime import datetime

import helpers.helper_achievements as helper_achievements
import helpers.helper_connections as helper_connections
import helpers.helper_general as helper_general
import helpers.helper_profile as helper_profile
import helpers.helper_posts as helper_posts
import helpers.helper_flashcards as helper_flashcards
import helpers.helper_quizzes as helper_quizzes
from flask import Blueprint, redirect, render_template, request, session

profile_blueprint = Blueprint(
    "profile", __name__, static_folder="static", template_folder="templates"
)


@profile_blueprint.route("/profile", methods=["GET"])
def user_profile() -> object:
    """
    Checks the user is logged in before viewing their profile page.

    Returns:
        Redirection to their profile if they're logged in.
    """
    if "username" in session:
        return redirect("/profile/" + session["username"])

    return redirect("/")


@profile_blueprint.route("/profile/<username>", methods=["GET"])
def profile(username: str) -> object:
    """
    Displays the user's profile page and fills in all of the necessary
    details. Hides the request buttons if the user is seeing their own page
    and checks if the user viewing the page has unlocked any achievements.

    Args:
        username: The user to view the profile of.

    Returns:
        The updated web page based on whether the details provided were valid,
        and the profile page user's privacy settings.
    """
    email = ""
    conn_type = ""
    hobbies = []
    interests = []
    message = []

    if "register_details" in session:
        session.pop("register_details", None)

    with connect_to_db() as conn:
        cur = conn.cursor()
        # Gets user from database using username.
        cur.execute(
            "SELECT name, bio, gender, birthday, profilepicture, privacy FROM "
            "user_profile WHERE username=%s;",
            (username,),
        )
        row = cur.fetchall()
        if len(row) == 0:
            message.append("Tên tài khoản " + username + " không tồn tại.")
            message.append("Vui lòng đảm bảo bạn đã nhập tên chính xác.")
            session["prev-page"] = request.url
            session["error"] = message
            return render_template(
                "error.html",
                message=message,
                requestCount=helper_connections.get_connection_request_count(),
                notifications=helper_general.get_notifications(),
            )
        else:
            data = row[0]
            name, bio, gender, birthday, profile_picture, privacy = (
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
            )

    # If the user is logged in, specific features can then be displayed.
    if session.get("username"):
        if username == session["username"]:
            # Gets the user's posts regardless of post settings if user is the
            # owner of the profile.
            cur.execute(
                "SELECT * FROM posts WHERE username=%s AND privacy!='deleted'",
                (username,),
            )
            sort_posts = cur.fetchall()
        else:
            # Gets the connection type between the profile owner and the user.
            their_close_friend = helper_connections.is_close_friend(
                username, session["username"]
            )
            your_close_friend = helper_connections.is_close_friend(
                session["username"], username
            )
            if not your_close_friend:
                conn_type = helper_connections.get_connection_type(username)
                if conn_type == "blocked":
                    message.append(
                        "Không thể xem trang cá nhân của "
                        + username
                        + " vì bạn đã bị chặn."
                    )
                    session["prev-page"] = request.url
                    return render_template(
                        "error.html",
                        message=message,
                        requestCount=helper_connections.get_connection_request_count(),
                        notifications=helper_general.get_notifications(),
                    )
                elif privacy in ("close_friends", "private"):
                    message.append("Trang cá nhân này là riêng tư")
                    session["prev-page"] = request.url
                    return render_template(
                        "error.html",
                        message=message,
                        requestCount=helper_connections.get_connection_request_count(),
                        notifications=helper_general.get_notifications(),
                    )
            else:
                conn_type = "close_friend"
                if privacy == "private":
                    message.append("Trang cá nhân này là riêng tư.")
                    session["prev-page"] = request.url
                    return render_template(
                        "error.html",
                        message=message,
                        requestCount=helper_connections.get_connection_request_count(),
                        notifications=helper_general.get_notifications(),
                    )

            session["prev-page"] = request.url
            connections = helper_general.get_all_connections(username)
            count = 0
            for connection in connections:
                connections[count] = connection[0]
                count += 1
            if session["username"] in connections:
                # check if user trying to view profile is a close friend
                if their_close_friend:
                    cur.execute(
                        "SELECT * "
                        "FROM posts WHERE username=%s "
                        "AND privacy not in "
                        "('private', 'deleted');",
                        (username,),
                    )
                    sort_posts = cur.fetchall()
                else:
                    cur.execute(
                        "SELECT * "
                        "FROM posts WHERE username=%s "
                        "AND privacy not in "
                        "('private', 'deleted', 'close');",
                        (username,),
                    )
                    sort_posts = cur.fetchall()
            else:
                cur.execute(
                    "SELECT * FROM posts WHERE username=%s AND privacy='public' ",
                    (username,),
                )
                sort_posts = cur.fetchall()

        helper_achievements.update_profile_achievements(username)
    else:
        # Only public posts can be viewed when not logged in
        cur.execute(
            "SELECT * FROM posts WHERE username=%s AND privacy='public'", (username,)
        )
        sort_posts = cur.fetchall()

    # Sort reverse chronologically
    sort_posts.sort(key=lambda x: x[0], reverse=True)

    user_posts = {"UserPosts": []}

    for user_post in sort_posts:
        add = ""
        if len(user_post[1]) > 250:
            add = "..."

        if user_post[5] == "protected":
            privacy = "Friends only"
            icon = "user plus"
        elif user_post[5] == "close":
            privacy = "Close friends only"
            icon = "handshake outline"
        elif user_post[5] == "private":
            privacy = "Private"
            icon = "lock"
        elif user_post[5] == "deleted":
            privacy = "Deleted"
            icon = "small trash alternate outline icon"
        else:
            privacy = str(user_post[5]).capitalize()
            icon = "users"

        # Get number of comments
        cur.execute("SELECT * FROM comments WHERE post_id=%s;", (user_post[0],))
        comment_count = len(cur.fetchall())

        liked = helper_posts.check_if_liked(cur, user_post[0], session.get("username"))

        time = user_post[4].strftime("%d-%m-%y")
        user_posts["UserPosts"].append(
            {
                "postId": user_post[0],
                "title": (user_post[1])[:250] + add,
                "profile_pic": "https://via.placeholder.com/600",
                "author": user_post[3],
                "likes": user_post[2],
                "comments": comment_count,
                "liked": liked,
                "account_type": helper_posts.get_account_type(user_post[3]),
                "date_posted": time,
                "privacy": privacy,
                "icon": icon,
            }
        )

    # Gets total (visible) post count
    total_posts = len(user_posts["UserPosts"])

    # Gets account type.
    cur.execute("SELECT type FROM accounts WHERE username=%s;", (username,))
    row = cur.fetchall()
    account_type = row[0][0]

    # Gets users degree.
    cur.execute(
        "SELECT degree FROM  "
        "degree WHERE degree_id = (SELECT degree "
        "FROM user_profile WHERE username=%s);",
        (username,),
    )
    row = cur.fetchone()
    degree = row[0]

    # Gets the user's hobbies.
    cur.execute("SELECT hobby FROM user_hobby WHERE username=%s;", (username,))
    row = cur.fetchall()
    if len(row) > 0:
        hobbies = row

    # Gets the user's interests.
    cur.execute("SELECT interest FROM user_interests WHERE username=%s;", (username,))
    row = cur.fetchall()
    if len(row) > 0:
        interests = row

    # Gets the user's email
    cur.execute("SELECT email from accounts WHERE username=%s;", (username,))
    row = cur.fetchall()
    if len(row) > 0:
        email = row[0][0]

    # Gets socials of the user
    socials = helper_profile.read_socials(username)

    # Gets flashcard sets made by the user
    flashcards = helper_flashcards.get_user_cards(username)[:2]

    # Gets quizzes made by the user
    quizzes = helper_quizzes.get_user_quizzes(username)[:2]

    # Gets the user's six rarest achievements.
    unlocked_achievements, _ = helper_achievements.get_achievements(username)
    first_six = unlocked_achievements[0 : min(6, len(unlocked_achievements))]

    # Calculates the user's age based on their date of birth.
    datetime_object = birthday
    age = helper_profile.calculate_age(datetime_object)

    # get user level
    helper_general.check_level_exists(username, conn)

    level_data = helper_profile.get_level(username)
    level = level_data[0]
    current_xp = level_data[1]
    xp_next_level = level_data[2]

    percentage_level = 100 * float(current_xp) / float(xp_next_level)
    progress_color = "green"
    if percentage_level < 75:
        progress_color = "orange"
    if percentage_level < 50:
        progress_color = "yellow"
    if percentage_level < 25:
        progress_color = "red"

    if session.get("username"):
        session["prev-page"] = request.url
        return render_template(
            "profile.html",
            username=username,
            name=name,
            bio=bio,
            gender=gender,
            birthday=birthday,
            profile_picture=profile_picture,
            age=age,
            hobbies=hobbies,
            account_type=account_type,
            interests=interests,
            degree=degree,
            email=email,
            socials=socials,
            flashcards=flashcards,
            quizzes=quizzes,
            posts=user_posts,
            total_posts=total_posts,
            type=conn_type,
            unlocked_achievements=first_six,
            allUsernames=helper_general.get_all_usernames(),
            requestCount=helper_connections.get_connection_request_count(),
            level=level,
            current_xp=int(current_xp),
            xp_next_level=int(xp_next_level),
            progress_color=progress_color,
            notifications=helper_general.get_notifications(),
        )
    else:
        session["prev-page"] = request.url
        return render_template(
            "profile.html",
            username=username,
            name=name,
            bio=bio,
            gender=gender,
            birthday=birthday,
            profile_picture=profile_picture,
            age=age,
            hobbies=hobbies,
            account_type=account_type,
            interests=interests,
            socials=socials,
            flashcards=flashcards,
            quizzes=quizzes,
            degree=degree,
            email=email,
            posts=user_posts,
            total_posts=total_posts,
            type="none",
            unlocked_achievements=first_six,
            level=level,
            current_xp=int(current_xp),
            xp_next_level=int(xp_next_level),
            progress_color=progress_color,
            notifications=helper_general.get_notifications(),
        )


@profile_blueprint.route("/edit-profile", methods=["GET", "POST"])
def edit_profile() -> object:
    """
    Updates the user's profile using info from the edit profile form.

    Returns:
        The updated profile page if the details provided were valid.
    """
    degrees = {"degrees": []}
    with connect_to_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT birthday, bio, degree, privacy, gender FROM user_profile "
            "WHERE username=%s;",
            (session["username"],),
        )
        data = cur.fetchone()
        dob = data[0]
        bio = data[1]
        degree = data[2]
        privacy = data[3]
        gender = data[4]

        cur.execute(
            "SELECT hobby FROM user_hobby WHERE username=%s;", (session["username"],)
        )
        hobbies = cur.fetchall()

        cur.execute(
            "SELECT interest FROM user_interests WHERE username=%s;",
            (session["username"],),
        )
        interests = cur.fetchall()

        # gets all possible degrees
        cur.execute(
            "SELECT * FROM degree",
        )
        degree_list = cur.fetchall()
        for item in degree_list:
            degrees["degrees"].append({"degreeId": item[0], "degree": item[1]})

    socials = helper_profile.read_socials(session["username"])

    # Renders the edit profile form if they navigated to this page.
    if request.method == "GET":
        return render_template(
            "settings.html",
            requestCount=helper_connections.get_connection_request_count(),
            date=dob,
            bio=bio,
            degrees=degrees,
            gender=gender,
            degree=degree,
            socials=socials,
            privacy=privacy,
            hobbies=hobbies,
            interests=interests,
            errors=[],
            notifications=helper_general.get_notifications(),
        )

    # Processes the form if they updated their profile using the form.
    if request.method == "POST":
        # Ensures that users can only edit their own profile.
        username = session["username"]
        # Gets the input data from the edit profile details form.
        bio = request.form.get("bio_input")

        # Award achievement ID 11 - Describe yourself if necessary
        if bio not in ("Thay đổi bio của bạn trong cài đặt.", ""):
            helper_achievements.apply_achievement(username, 11)

        gender = request.form.get("gender_input")
        dob_input = request.form.get("dob_input")
        dob = datetime.strptime(dob_input, "%Y-%m-%d").strftime("%Y-%m-%d")
        hobbies_input = request.form.get("hobbies_input")
        interests_input = request.form.get("interests_input")
        degree = request.form.get("degree_input")
        # Gets the individual hobbies and interests, then formats them.
        hobbies_unformatted = hobbies_input.split(",")
        hobbies = [hobby.lower() for hobby in hobbies_unformatted]
        interests_unformatted = interests_input.split(",")
        interests = [interest.lower() for interest in interests_unformatted]
        # Connects to the database to perform validation.
        with connect_to_db() as conn:
            cur = conn.cursor()

            # Validates user profile details and uploaded image.
            valid, message = helper_profile.validate_edit_profile(
                bio, gender, dob, hobbies, interests
            )
            if valid:
                file = request.files["file"]
                (
                    valid,
                    message,
                    file_name_hashed,
                ) = helper_profile.validate_profile_pic(file)
                if valid and file_name_hashed:
                    # Award achievement ID 18 - Show yourself if necessary
                    helper_achievements.apply_achievement(username, 18)

            # Updates the user profile if details are valid.
            if valid:
                # Updates the bio, gender, and birthday.
                if file_name_hashed:
                    cur.execute(
                        "UPDATE user_profile SET bio=%s, gender=%s, birthday=%s, "
                        "profilepicture=%s, degree=%s WHERE username=%s;",
                        (
                            bio,
                            gender,
                            dob,
                            "/static/images/avatars/" + file_name_hashed + ".jpg",
                            degree,
                            username,
                        ),
                    )
                    conn.commit()

                    helper_achievements.update_profile_achievements(username)

                else:
                    cur.execute(
                        "UPDATE user_profile SET bio=%s, gender=%s, birthday=%s, "
                        "degree=%s WHERE username=%s;",
                        (
                            bio,
                            gender,
                            dob,
                            degree,
                            username,
                        ),
                    )

                # Inserts new hobbies and interests into the database if the
                # user made a new input.

                cur.execute("DELETE FROM user_hobby WHERE username=%s;", (username,))
                cur.execute(
                    "DELETE FROM user_interests WHERE username=%s;", (username,)
                )
                if hobbies != [""]:
                    for hobby in hobbies:
                        cur.execute(
                            "SELECT hobby FROM user_hobby WHERE username=%s AND hobby=%s;",
                            (
                                username,
                                hobby,
                            ),
                        )
                        if cur.fetchone() is None:
                            cur.execute(
                                "INSERT INTO user_hobby (username, "
                                "hobby) VALUES (%s, %s);",
                                (
                                    username,
                                    hobby,
                                ),
                            )
                if interests != [""]:
                    for interest in interests:
                        cur.execute(
                            "SELECT interest FROM user_interests WHERE "
                            "username=%s AND interest=%s;",
                            (
                                username,
                                interest,
                            ),
                        )
                        if cur.fetchone() is None:
                            cur.execute(
                                "INSERT INTO user_interests "
                                "(username, interest) VALUES (%s, %s);",
                                (
                                    username,
                                    interest,
                                ),
                            )

                conn.commit()
                return redirect("/profile")
            # Displays error message(s) stating why their details are invalid.
            else:
                session["error"] = message
                return render_template(
                    "settings.html",
                    errors=message,
                    requestCount=helper_connections.get_connection_request_count(),
                    allUsernames=helper_general.get_all_usernames(),
                    degrees=degrees,
                    degree=degree,
                    date=dob,
                    bio=bio,
                    privacy=privacy,
                    socials=socials,
                    notifications=helper_general.get_notifications(),
                )


@profile_blueprint.route("/profile_privacy", methods=["POST"])
def profile_privacy() -> object:
    """
    Changes the privacy setting of the user's profile page.

    Returns:
        The web page to edit the user's profile details.
    """
    privacy = request.form.get("privacy")
    with connect_to_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE user_profile SET privacy=%s WHERE username=%s;",
            (
                privacy,
                session["username"],
            ),
        )

    return redirect("/profile")


@profile_blueprint.route("/edit_socials", methods=["POST"])
def edit_socials() -> object:
    """
    Changes the links to the user's social media profiles.

    Returns:
        The web page for the logged in user's profile page.
    """
    socials = {
        "twitter": request.form.get("twitter"),
        "facebook": request.form.get("facebook"),
        "youtube": request.form.get("youtube"),
        "instagram": request.form.get("instagram"),
        "linkedin": request.form.get("linkedin"),
    }
    with connect_to_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM user_social WHERE username=%s;", (session["username"],)
        )
        for key, value in socials.items():
            if value != "":
                cur.execute(
                    "INSERT INTO user_social (username, social, link) VALUES (%s, %s, %s);",
                    (session["username"], key, value),
                )

    return redirect("/profile")
