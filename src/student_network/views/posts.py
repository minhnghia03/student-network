"""
Handles the view for posts on the feed and related functionality.
"""

import re
from db import connect_to_db
from datetime import datetime

import helpers.helper_achievements as helper_achievements
import helpers.helper_connections as helper_connections
import helpers.helper_general as helper_general
import helpers.helper_posts as helper_posts
import helpers.helper_profile as helper_profile
from flask import Blueprint, jsonify, redirect, render_template, request, session

posts_blueprint = Blueprint(
    "posts", __name__, static_folder="static", template_folder="templates"
)


@posts_blueprint.route("/post_page/<post_id>", methods=["GET"])
def post(post_id: int) -> object:
    """
    Loads a post and comments on that post.

    Returns:
        Redirection to the post page.
    """
    comments = {"comments": []}
    message = []
    author = ""
    session["prev-page"] = request.url
    content = None
    # check post restrictions
    with connect_to_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT privacy, username FROM posts WHERE post_id=%s;", (post_id,))
        row = cur.fetchone()
        if row is None:
            return render_template(
                "error.html",
                message=["Bài viết này không tồn tại."],
                requestCount=helper_connections.get_connection_request_count(),
            )
        privacy = row[0]
        username = row[1]
        # check its if its an anonymous user or a logged in user
        if "username" not in session:
            return redirect("/login")
        if session.get("username"):
            # check if the user is the same as the author of the post
            if username != session["username"]:
                # check if post is available for display
                if privacy == "private":
                    return render_template(
                        "error.html",
                        message=[
                            "Bài viết này là riêng tư. Bạn không thể truy cập nó."
                        ],
                        requestCount=helper_connections.get_connection_request_count(),
                    )
                else:
                    # Checks if user trying to view the post has a connection
                    # with the post author.
                    conn_type = helper_connections.get_connection_type(username)
                    if conn_type != "connected":
                        if privacy == "protected":
                            return render_template(
                                "error.html",
                                message=[
                                    "Bài viết này chỉ có thể truy cập được bằng cách kết nối."
                                ],
                                requestCount=helper_connections.get_connection_request_count(),
                            )
                    else:
                        # If the user and author are connected, check that they
                        # are close friends.
                        connection = helper_connections.is_close_friend(
                            username, session["username"]
                        )
                        if connection is not True:
                            if privacy == "close":
                                return render_template(
                                    "error.html",
                                    message=[
                                        "Bài viết này chỉ có thể truy cập được với bạn thân."
                                    ],
                                    requestCount=helper_connections.get_connection_request_count(),
                                )
        else:
            if privacy != "public":
                return render_template(
                    "error.html",
                    message=["Bài viết này là riêng tư. Bạn không thể truy cập nó."],
                    requestCount=helper_connections.get_connection_request_count(),
                )

        # Gets user from database using username.
        cur.execute(
            "SELECT body, username, date, likes FROM posts WHERE post_id=%s;",
            (post_id,),
        )
        row = cur.fetchall()
        if len(row) == 0:
            message.append("Bài viết này không tồn tại.")
            message.append("Vui lòng đảm bảo bạn đã nhập tên chính xác.")
            session["prev-page"] = request.url
            return render_template(
                "error.html",
                message=message,
                requestCount=helper_connections.get_connection_request_count(),
                allUsernames=helper_general.get_all_usernames(),
                notifications=helper_general.get_notifications(),
            )
        else:
            data = row[0]
            (body, username, date_posted, account_type, likes) = (
                data[0],
                data[1],
                data[2],
                helper_posts.get_account_type(data[1]),
                data[3],
            )

            liked = helper_posts.check_if_liked(cur, post_id, session["username"])

            cur.execute(
                "SELECT username FROM accounts WHERE username=%s;",
                (session["username"],),
            )
            user_account_type = cur.fetchone()[0]

            cur.execute(
                "SELECT content_url from post_content WHERE post_id=%s;", (post_id,)
            )
            images = cur.fetchall()

            cur.execute("SELECT * FROM comments WHERE post_id=%s;", (post_id,))
            row = cur.fetchall()
            if len(row) == 0:
                session["prev-page"] = request.url
                return render_template(
                    "post_page.html",
                    author=author,
                    postId=post_id,
                    body=body,
                    username=username,
                    date=date_posted,
                    likes=likes,
                    liked=liked,
                    images=images,
                    account_type=account_type,
                    user_account_type=user_account_type,
                    comments=None,
                    requestCount=helper_connections.get_connection_request_count(),
                    allUsernames=helper_general.get_all_usernames(),
                    avatar=helper_profile.get_profile_picture(username),
                    content=content,
                    notifications=helper_general.get_notifications(),
                )
            for comment in row:
                time = comment[3]
                comments["comments"].append(
                    {
                        "commentId": comment[0],
                        "username": comment[1],
                        "body": comment[2],
                        "date": helper_general.display_short_notification_age(
                            (datetime.now() - time).total_seconds()
                        ),
                        "profilePic": helper_profile.get_profile_picture(comment[1]),
                    }
                )
            session["prev-page"] = request.url
            return render_template(
                "post_page.html",
                author=author,
                postId=post_id,
                body=body,
                username=username,
                liked=liked,
                date=date_posted,
                likes=likes,
                images=images,
                account_type=account_type,
                user_account_type=user_account_type,
                comments=comments,
                requestCount=helper_connections.get_connection_request_count(),
                allUsernames=helper_general.get_all_usernames(),
                avatar=helper_profile.get_profile_picture(username),
                content=content,
                notifications=helper_general.get_notifications(),
            )


@posts_blueprint.route("/fetch_posts/", methods=["GET"])
def json_posts() -> dict:
    """
    Creates a JSON format for each post to make them readable by JavaScript.

    Returns:
        JSON dictionary file for posts.
    """
    number = request.args.get("number")
    starting_id = request.args.get("starting_id")
    all_posts, _, _ = helper_posts.fetch_posts(number, starting_id)
    return jsonify(all_posts)


@posts_blueprint.route("/feed", methods=["GET"])
def feed() -> object:
    """
    Checks user is logged in before viewing their feed page.

    Returns:
        Redirection to their feed if they're logged in.
    """
    session["prev-page"] = request.url
    with connect_to_db() as conn:
        cur = conn.cursor()

        connections = helper_general.get_all_connections(session["username"])
        connections.append((session["username"],))
        cur.execute("SELECT MAX(post_id) FROM posts")
        row = cur.fetchone()

    _, content, valid = helper_posts.fetch_posts(2, row[0])
    # Displays any error messages.
    if valid:
        if "error" in session:
            errors = session["error"]
            session.pop("error", None)
            session["prev-page"] = request.url
            return render_template(
                "feed.html",
                requestCount=helper_connections.get_connection_request_count(),
                allUsernames=helper_general.get_all_usernames(),
                errors=errors,
                content=content,
                max_id=row[0],
                notifications=helper_general.get_notifications(),
            )
        else:
            session["prev-page"] = request.url
            return render_template(
                "feed.html",
                requestCount=helper_connections.get_connection_request_count(),
                allUsernames=helper_general.get_all_usernames(),
                content=content,
                max_id=row[0],
                notifications=helper_general.get_notifications(),
            )
    else:
        return redirect("/login")


@posts_blueprint.route("/search_query", methods=["GET"])
def search_query() -> dict:
    """
    Searches for members registered in the student network.

    Returns:
        JSON dictionary of search results of users, and their hobbies
        and interests.
    """
    with connect_to_db() as conn:
        cur = conn.cursor()
        chars = request.args.get("chars")
        hobby = request.args.get("hobby")
        interest = request.args.get("interest")
        name_pattern = "%" + chars + "%"
        hobby_pattern = "%" + hobby + "%"
        interest_pattern = "%" + interest + "%"

        # Filters by username, common hobbies, and interests.
        cur.execute(
            "SELECT user_profile.username, user_hobby.hobby, "
            "user_interests.interest FROM user_profile "
            "LEFT JOIN user_hobby ON user_hobby.username=user_profile.username "
            "LEFT JOIN user_interests ON "
            "user_interests.username=user_profile.username "
            "WHERE (user_profile.username LIKE %s) "
            "AND (IFNULL(hobby, '') LIKE %s) AND (IFNULL(interest, '') LIKE %s) "
            "GROUP BY user_profile.username LIMIT 10;",
            (
                name_pattern,
                hobby_pattern,
                interest_pattern,
            ),
        )
        usernames = cur.fetchall()
        # Sorts results alphabetically.
        usernames.sort(key=lambda x: x[0])  # [(username, degree)]
        # Adds a profile picture to each user.
        usernames = list(
            map(
                lambda x: (
                    x[0],
                    x[1],
                    x[2],
                    helper_profile.get_profile_picture(x[0]),
                    helper_profile.get_degree(x[0])[1],
                ),
                usernames,
            )
        )

    return jsonify(usernames)


@posts_blueprint.route("/submit_post", methods=["POST"])
def submit_post() -> object:
    """
    Submit post on social wall to database.

    Returns:
        Updated feed with new post added
    """
    post_privacy = request.form.get("privacy")
    post_body = request.form["post_text"]
    all_file_names = request.form["allFileNames"]

    all_file_names_split = all_file_names.split(",")

    # Only adds the post if a title has been input.
    if len(all_file_names) > 0 or len(post_body) > 0:
        with connect_to_db() as conn:
            cur = conn.cursor()
            # Get account type
            cur.execute(
                "SELECT type FROM accounts WHERE username=%s;",
                (session["username"],),
            )
            cur.execute("SELECT COUNT(*) FROM posts")
            row_count = int(cur.fetchone()[0])
            row_id = row_count + 1
            cur.execute(
                "INSERT INTO posts (post_id, body, username,"
                "privacy) VALUES (%s, %s, %s, %s);",
                (
                    row_id,
                    post_body,
                    session["username"],
                    post_privacy,
                ),
            )

            if len(all_file_names) > 0:
                for fileName in all_file_names_split:
                    cur.execute(
                        "INSERT INTO post_content (post_id, content_url) VALUES (%s, %s);",
                        (
                            row_id,
                            fileName,
                        ),
                    )

            conn.commit()
            usernames_tagged = re.findall(r"@(\w+)", post_body)
            for username in usernames_tagged:
                helper_general.new_notification_username(
                    username,
                    "Bạn đã được đề cập bởi {} trong bài viết!".format(
                        session["username"]
                    ),
                    "/post_page/{}".format(row_id),
                )
            helper_posts.update_submission_achievements(cur)
    else:
        # Prints error message stating that the title is missing.
        session["error"] = ["Đảm bảo tất cả các trường đã được điền chính xác!"]

    return redirect("/feed")


@posts_blueprint.route("/like_post", methods=["POST"])
def like_post() -> object:
    """
    Processes liking a post to the database.

    Returns:
        Redirection to the post with like added.
    """
    post_id = request.form["postId"]

    with connect_to_db() as conn:
        cur = conn.cursor()
        liked = helper_posts.check_if_liked(cur, post_id, session["username"])
        if not liked:
            cur.execute(
                "INSERT INTO user_likes (post_id,username) VALUES (%s, %s);",
                (post_id, session["username"]),
            )

            # Gets number of current likes.
            cur.execute(
                "SELECT likes, username FROM posts WHERE post_id=%s;", (post_id,)
            )
            row = cur.fetchone()
            likes = row[0] + 1
            username = row[1]

            cur.execute(
                "UPDATE posts SET likes=%s WHERE post_id=%s ;",
                (
                    likes,
                    post_id,
                ),
            )
            conn.commit()

            cur.execute(
                "SELECT username FROM all_user_likes WHERE post_id=%s;", (post_id,)
            )
            row = cur.fetchall()
            names = [x[0] for x in row]
            if session["username"] not in names:
                # 1 exp earned for the author of the post
                helper_general.check_level_exists(username, conn)
                helper_general.one_exp(cur, username)
                cur.execute(
                    "INSERT INTO all_user_likes (post_id,username) VALUES (%s, %s);",
                    (post_id, session["username"]),
                )
                conn.commit()

            helper_achievements.update_post_achievements(cur, likes, username)
        else:
            # Gets number of current likes.
            cur.execute("SELECT likes FROM posts WHERE post_id=%s;", (post_id,))
            row = cur.fetchone()
            likes = row[0] - 1

            cur.execute(
                "UPDATE posts SET likes=%s WHERE post_id=%s ;",
                (
                    likes,
                    post_id,
                ),
            )
            conn.commit()

            cur.execute(
                "DELETE FROM user_likes WHERE (post_id=%s AND username=%s)",
                (post_id, session["username"]),
            )
            conn.commit()

    return redirect("/post_page/" + post_id)


@posts_blueprint.route("/submit_comment", methods=["POST"])
def submit_comment() -> object:
    """
    Submit comment on post page to database.

    Returns:
        Updated post with new comment added
    """
    post_id = request.form["postId"]
    comment_body = request.form["comment_text"]

    # Only submits the comment if it is not empty.
    if comment_body.replace(" ", "") != "":
        with connect_to_db() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO comments (post_id, body, username) VALUES (%s, %s, %s);",
                (post_id, comment_body, session["username"]),
            )
            conn.commit()

            # Get username on post
            cur.execute("SELECT username FROM posts WHERE post_id=%s;", (post_id,))
            username = cur.fetchone()[0]

            # Get number of comments
            cur.execute(
                "SELECT COUNT(comment_id) FROM comments WHERE post_id=%s;", (post_id,)
            )
            row = cur.fetchone()[0]

            helper_posts.update_comment_achievements(row, username)

            # we haven't commented on our own post
            if username != session["username"]:
                helper_general.new_notification_username(
                    username,
                    "{} đã bình luận trên bài viết của bạn!".format(
                        session["username"]
                    ),
                    "/post_page/{}".format(post_id),
                )

    session["postId"] = post_id
    return redirect("/post_page/" + post_id)


@posts_blueprint.route("/delete_post", methods=["POST"])
def delete_post() -> object:
    """
    Deletes a post from the database.

    Returns:
        Renders a page stating that the post has been deleted successfully.
    """
    post_id = request.form["postId"]
    message = []

    with connect_to_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT post_id FROM posts WHERE post_id=%s;", (post_id,))
        row = cur.fetchone()
        # check the post exists in database
        if row[0] is None:
            message.append("Lỗi: bài viết này không tồn tại")
        else:
            cur.execute(
                "UPDATE posts SET privacy=%s WHERE post_id=%s;", ("deleted", post_id)
            )
            conn.commit()

    message.append("Bài viết đã được xóa thành công.")
    session["prev-page"] = request.url
    return render_template(
        "error.html",
        message=message,
        requestCount=helper_connections.get_connection_request_count(),
        allUsernames=helper_general.get_all_usernames(),
        notifications=helper_general.get_notifications(),
    )


@posts_blueprint.route("/delete_comment", methods=["POST"])
def delete_comment() -> object:
    """
    Deletes a comment from the database.

    Returns:
        Redirection to the post page.
    """
    message = []
    post_id = request.form["postId"]
    comment_id = request.form["commentId"]

    with connect_to_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM comments WHERE comment_id=%s ", (comment_id,))
        row = cur.fetchone()
        # Checks that the comment exists.
        if row[0] is None:
            message.append("Bình luận không tồn tại.")
            session["prev-page"] = request.url
            return render_template(
                "error.html",
                message=message,
                requestCount=helper_connections.get_connection_request_count(),
                allUsernames=helper_general.get_all_usernames(),
                notifications=helper_general.get_notifications(),
            )
        else:
            cur.execute("DELETE FROM comments WHERE comment_id =%s ", (comment_id,))
            conn.commit()

    return redirect("post_page/" + post_id)


@posts_blueprint.route("/upload_file", methods=["POST"])
def upload_file():
    """
    An API that sends the files using a form, they are then saved here
    and a list of names of the files is returned
    """
    max_file_upload = 10
    file_names = []
    if request.files:
        for file_name in request.files:
            file = request.files[file_name]

            file_name = helper_posts.upload_image(file)
            file_names.append(file_name)

            max_file_upload -= 1
            if max_file_upload <= 0:
                break

    return jsonify(file_names)


@posts_blueprint.route("/delete_file", methods=["POST"])
def delete_file():
    """
    An API call to delete a file with a given name from the server
    """
    file_name = request.args.get("filename")
    # try and prevent escaping this path
    file_name.replace(".", "")
    file_name.replace("/", "")
    helper_posts.delete_file(file_name + ".jpg")
    return "200"


@posts_blueprint.route("/user_exists", methods=["GET"])
def user_exists():
    username = request.args.get("username")

    with connect_to_db() as conn:
        cur = conn.cursor()

        cur.execute("SELECT username FROM accounts WHERE username=%s;", (username,))

        row = cur.fetchone()

        if row is None:
            return "False"

        return "True"

    return "False"
