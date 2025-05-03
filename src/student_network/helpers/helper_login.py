"""
Performs checks and actions to help the login system work effectively.
"""

import re
from typing import Tuple, List

from email_validator import validate_email, EmailNotValidError


def validate_registration(
    cur,
    username: str,
    full_name: str,
    password: str,
    password_confirm: str,
    email: str,
    terms: str,
) -> Tuple[bool, List[str]]:
    """
    Validates the registration details to ensure that the email address is
    valid, and that the passwords in the form match.

    Args:
        cur: Cursor for the SQLite database.
        username: The username input by the user in the form.
        full_name: The full name input by the user in the form.
        password: The password input by the user in the form.
        password_confirm: The password confirmation input by the user in the
                          form.
        email: The email address input by the user in the form.
        terms: The terms and conditions input checkbox.

    Returns:
        Whether the registration was valid, and the error message(s) if not.
    """
    # Registration remains valid as long as it isn't caught by any checks. If
    # not, error messages will be provided to the user.
    valid = True
    message = []

    # Checks that there are no null inputs.
    if (
        username == ""
        or full_name == ""
        or password == ""
        or password_confirm == ""
        or email == ""
    ):
        message.append("Một số trường chưa được điền!")
        valid = False

    # Checks that the username only contains valid characters.
    if username.isalnum() is False:
        message.append("Tên tài khoản chỉ được chứa chữ cái và số!")
        valid = False
    # Checks that the username hasn't already been registered.
    cur.execute("SELECT * FROM accounts WHERE username=%s;", (username,))
    if cur.fetchone() is not None:
        message.append("Tên tài khoản đã được đăng ký!")
        valid = False

    # Checks that the full name doesn't exceed 40 characters.
    if len(full_name) > 40:
        message.append("Tên đầy đủ vượt quá 40 ký tự!")
        valid = False
    # Checks that the full name only contains valid characters.
    if not all(x.isalpha() or x.isspace() for x in full_name):
        message.append("Tên đầy đủ chỉ được chứa chữ cái và khoảng trắng!")
        valid = False

    # Checks that the email hasn't already been registered.
    cur.execute("SELECT * FROM accounts WHERE email=%s;", (email,))
    if cur.fetchone() is not None:
        message.append("Email đã được đăng ký!")
        valid = False
    # Checks that the email address has the correct format, checks whether it
    # exists, and isn't a blacklist email.
    try:
        valid_email = validate_email(email)
        # Updates with the normalised form of the email address.
        email = valid_email.email
        # If the format is valid, checks that the email address has the
        # University of Exeter domain.
        if re.search("@.*", email) is not None:
            domain = re.search("@.*", email).group()
            domain_type = domain.split(".")[1]
            if domain_type not in ["ac", "edu"]:
                valid = False
                message.append("Email không thuộc trường đại học đã đăng ký!")
    except EmailNotValidError:
        message.append("Email không hợp lệ!")
        valid = False

    # Checks that the password has a minimum length of 8 characters, and at
    # least one number.
    if len(password) <= 7 or any(char.isdigit() for char in password) is False:
        message.append(
            "Mật khẩu không đáp ứng yêu cầu! Nó phải chứa ít nhất 8 ký tự, "
            "bao gồm ít nhất một số."
        )
        valid = False
    # Checks that the passwords match.
    if password != password_confirm:
        message.append("Mật khẩu không khớp!")
        valid = False

    # Checks that the terms of service has been ticked.
    if terms is None:
        message.append("Bạn phải chấp nhận điều khoản dịch vụ!")
        valid = False

    return valid, message
