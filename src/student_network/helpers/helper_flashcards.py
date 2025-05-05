"""
Performs checks and actions to help flashcard sets work effectively.
"""

from db import connect_to_db
from datetime import date
from typing import Tuple

from flask import request, session


def get_set_details(cur, set_id: int) -> Tuple[str, date, str, dict, int]:
    """
    Gets the details for the flashcard set being used.
    Args:
        cur: Cursor for the SQLite database.
        set_id: The ID of the flashcard set being used.

    Returns:
        Questions with answers, author, and name of the set.
    """
    cur.execute("SELECT * FROM question_sets WHERE set_id=%s;", (set_id,))
    set_details = cur.fetchone()

    if set_details[4]:
        questions = set_details[4].split("|")
    else:
        questions = ""
    if set_details[5]:
        answers = set_details[5].split("|")
    else:
        answers = ""
    questions_and_answers = {}
    for c, question in enumerate(questions):
        questions_and_answers[question] = answers[c]

    return (
        set_details[1],
        set_details[2],
        set_details[3],
        questions_and_answers,
        set_details[6],
    )


def delete_set(set_id):
    """
    Delete specific set

    Args:
        set_id: ID of the set to delete
    """
    with connect_to_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT author FROM question_sets WHERE set_id=%s;", (set_id,))
        author = cur.fetchone()[0]
        if author == session["username"]:
            cur.execute("DELETE FROM question_sets WHERE set_id=%s;", (set_id,))
            conn.commit()
        else:
            session["error"] = ["Bạn không thể xóa bộ flashcard của người khác"]


def delete_question(set_id, index):
    """
    Delete specific set

    Args:
        set_id: ID of the set to delete from
        index: the index of the question to delete
    """
    with connect_to_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT author FROM question_sets WHERE set_id=%s;", (set_id,))
        author = cur.fetchone()[0]
        if author == session["username"]:
            cur.execute(
                "SELECT questions, answers FROM question_sets WHERE set_id=%s;",
                (set_id,),
            )
            set_details = cur.fetchone()
            if not all(set_details[0]):
                session["error"] = ["Câu hỏi không tồn tại"]

            questions = set_details[0].split("|")
            answers = set_details[1].split("|")

            if len(questions) > index:
                questions.pop(index)
                questions = "|".join(questions)

                answers.pop(index)
                answers = "|".join(answers)
            else:
                session["error"] = ["Câu hỏi không tồn tại"]

            cur.execute(
                "UPDATE question_sets SET questions=%s, answers=%s WHERE set_id=%s;",
                (questions, answers, set_id),
            )
            conn.commit()

        else:
            session["error"] = ["Bạn không thể xóa bộ flashcard của người khác"]


def save_set(set_id):
    """
    Save changes to question set

    Args:
        set_id: ID of the set to save
    """
    # Gets set details.
    with connect_to_db() as conn:
        cur = conn.cursor()
        count = get_question_count(cur, set_id)

    questions, answers = "", ""
    for i in range(count):
        new_q = str(request.form.get("question_" + str(i)))
        if new_q:
            new_q = validate_inputs(new_q)
            questions += new_q + "|"
        else:
            questions += "|"
        new_a = str(request.form.get("answer_" + str(i)))
        if new_a:
            new_a = validate_inputs(new_a)
            answers += new_a + "|"
        else:
            answers += "|"
    if questions:
        if questions[-1] == "|":
            questions = questions[:-1]
    if answers:
        if answers[-1] == "|":
            answers = answers[:-1]

    if request.form.get("set_name"):
        name = request.form.get("set_name")
    else:
        name = "Unnamed"

    cur.execute(
        "UPDATE question_sets SET set_name=%s, questions=%s, answers=%s WHERE set_id=%s;",
        (name, questions, answers, set_id),
    )
    conn.commit()


def generate_set() -> int:
    """
    Generate new set with logged in user as author

    Returns:
        set_id of new set
    """
    with connect_to_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO question_sets (date_created,author) VALUES (%s, %s);",
            (date.today(), session["username"]),
        )
        cur.execute("SELECT MAX(set_id) FROM question_sets;")
        new_id = cur.fetchone()[0]

    return new_id


def add_card(set_id):
    """
    Add card to specific set

    Args:
        set_id: ID of the set to add to
    """
    with connect_to_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT questions, answers, author FROM question_sets WHERE set_id=%s;",
            (set_id,),
        )
        row = cur.fetchone()

        author = row[2]
        if author == session["username"]:
            if row[0] != "None" and row[1] != "None":
                question_list = row[0].split("|")
                answer_list = row[1].split("|")
                count = len(question_list) + 1
                if not "question " + str(count) in question_list:
                    questions = row[0] + "|question " + str(count)
                else:
                    q = "question " + str(count)
                    while q in question_list:
                        q = q + " 2"
                    questions = row[0] + "|" + q

                if not "answer " + str(count) in answer_list:
                    answers = row[1] + "|answer " + str(count)
                else:
                    a = "answer " + str(count)
                    while a in answer_list:
                        a = a + " 2"
                    answers = row[1] + "|" + a

            else:
                questions = "question1"
                answers = "answer1"

            cur.execute(
                "UPDATE question_sets SET questions=%s, answers=%s WHERE set_id=%s;",
                (questions, answers, set_id),
            )
            conn.commit()

        else:
            session["error"] = ["Bạn không thể thêm câu hỏi vào bộ flashcard của người khác"]


def add_play(cur, set_id):
    """
    Add 1 to plays for a set

    Args:
        set_id: ID of the set to increment
    """
    # Updates the number of times a quiz has been played.
    cur.execute(
        "UPDATE question_sets SET cards_played = cards_played + 1 WHERE set_id=%s;",
        (set_id,),
    )


def get_question_count(cur, set_id) -> int:
    """
    Get number of questions in a set

    Args:
        set_id: ID of the set to count
    """
    cur.execute("SELECT questions FROM question_sets WHERE set_id=%s;", (set_id,))
    set_details = cur.fetchone()
    if set_details[0] is None:
        return 0

    return len(set_details[0].split("|"))


def validate_inputs(text: str) -> str:
    """
    Cut the flashcard to max size of 600 characters and remove '|'
    characters since they split questions in the database

    Args:
        text: input string

    Returns:
        Reformatted string
    """
    text = text[:600]
    return text.replace("|", "")


def get_user_cards(username: str) -> list:
    """
    Get the flashcard sets of a given user

    Args:
        username: username to get sets from

    Returns:
        list of sets belonging to the user
    """
    with connect_to_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT set_id, date_created, author, set_name, cards_played "
            "FROM question_sets WHERE author=%s;",
            (username,),
        )
        row = cur.fetchall()
        set_posts = sorted(row, key=lambda x: x[4], reverse=True)
        set_posts = [list(x) for x in set_posts]

        for i, card_set in enumerate(set_posts):
            set_posts[i].append(get_question_count(cur, card_set[0]))

    return set_posts
