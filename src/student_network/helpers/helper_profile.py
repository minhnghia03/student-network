"""
Performs checks and actions to help the profile system work effectively.
"""

import uuid
from datetime import date, datetime
from typing import List, Tuple

import helpers.helper_general as helper_general
from PIL import Image
from werkzeug.utils import secure_filename
from db import connect_to_db
import os
from constants import BASE_DIR


def calculate_age(born: datetime) -> int:
    """
    Calculates the user's current age based on their date of birth.

    Args:
        born: The user's date of birth.

    Returns:
        The age of the user in years.
    """
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def get_degree(username: str) -> Tuple[int, str]:
    """
    Gets the degree of a user.

    Args:
        username: The username of the user's profile picture.

    Returns:
        The degree of the user.
        The degreeID of the user.
    """
    with connect_to_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT degree FROM user_profile WHERE username=%s;", (username,))
        degree_id = cur.fetchone()
        if degree_id:
            cur.execute(
                "SELECT degree FROM degree WHERE degree_id=%s;", (degree_id[0],)
            )
            degree = cur.fetchone()
            return degree_id[0], degree[0]


def get_level(username: str) -> List[int]:
    """
    Gets the current user experience points, the experience points
    for the next level and the user's current level from the database.

    Args:
        username: The username of the user logged in.

    Returns:
        The user's level, XP, and XP to reach the next level.
    """
    level = 1
    xp_next_level = 100
    xp_increase_per_level = 15

    exp = helper_general.get_exp(username)
    while exp >= xp_next_level:
        level += 1
        exp -= xp_next_level
        xp_next_level += xp_increase_per_level

    return [level, exp, xp_next_level]


def get_profile_picture(username: str) -> str:
    """
    Gets the profile picture of a user.

    Args:
        username: The username of the user's profile picture.

    Returns:
        The profile picture of the user.
    """
    with connect_to_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT profilepicture FROM user_profile WHERE username=%s;", (username,)
        )
        row = cur.fetchone()
        if row:
            return row[0]


def read_socials(username: str):
    """
    Args:
        username: The username whose socials to check.

    Returns:
        The social media accounts of that user.
    """
    with connect_to_db() as conn:
        cur = conn.cursor()
        socials = {}
        # Gets the user's socials
        cur.execute(
            "SELECT social, link from user_social WHERE username=%s;", (username,)
        )
        row = cur.fetchall()
        if len(row) > 0:
            for item in row:
                socials[item[0]] = item[1]
    return socials


def validate_edit_profile(
    bio: str, gender: str, dob: str, hobbies: list, interests: list
) -> Tuple[bool, List[str]]:
    """
    Validates the details in the profile editing form.

    Args:
        bio: The bio input by the user in the form.
        gender: The gender input selected by the user in the form.
        dob: The date of birth input selected by the user in the form.
        hobbies: The list of hobbies from the form.
        interests: The list of interests from the form.

    Returns:
        Whether profile editing was valid, and the error message(s) if not.
    """
    # Editing profile remains valid as long as it isn't caught by any checks.
    # If not, error messages will be provided to the user.
    valid = True
    message = []

    # Checks that the bio has a maximum of 160 characters.
    if len(bio) > 160:
        valid = False
        message.append("Bio không được vượt quá 160 ký tự!")

    # Checks that the gender is male, female, or other.
    if gender not in ["Nam", "Nữ", "Khác"]:
        valid = False
        message.append("Giới tính phải là nam, nữ hoặc khác!")

    # Only performs check if a new date of birth was entered.
    if dob:
        # Checks that date of birth is a past date.
        if datetime.today() < dob:
            valid = False
            message.append("Ngày sinh phải là ngày trong quá khứ!")

    # Checks that each hobby has a maximum of 24 characters.
    for hobby in hobbies:
        if len(hobby) > 24:
            valid = False
            message.append("Sở thích không được vượt quá 24 ký tự!")
            break
    # Checks that each interest has a maximum of 24 characters.
    for interest in interests:
        if len(interest) > 24:
            valid = False
            message.append("Sở thích không được vượt quá 24 ký tự!")
            break

    return valid, message


def validate_profile_pic(file) -> Tuple[bool, List[str], str]:
    """
    Validates the file to check that it's a valid image.

    Args:
        file: The file uploaded by the user.

    Returns:
        Whether the file uploaded is a valid image, and any error messages.
    """
    valid = True
    message = []
    file_name_hashed = ""

    # Hashes the name of the file and resizes it.
    if helper_general.is_allowed_photo_file(file.filename):
        secure_filename(file.filename)
        file_name_hashed = str(uuid.uuid4())
        file_path = os.path.join(
            BASE_DIR,
            "static",
            "images",
            "avatars",
            file_name_hashed,
        )
        img = Image.open(file)
        img = img.resize((400, 400))
        img = img.convert("RGB")
        img.save(file_path + ".jpg")
    elif file:
        valid = False
        message.append("Tệp tin phải là hình ảnh.")

    return valid, message, file_name_hashed
