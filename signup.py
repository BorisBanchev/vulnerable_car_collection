from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash
from db import db
from validate import create_account_valid
def create_account(username: str, password: str, password2: str):
    sql = text("INSERT INTO users (username, password_hash) VALUES (:username, :password)")
    valid = create_account_valid(username, password, password2)
    if valid[2]:
        db.session.execute(sql, {"username":username, "password":generate_password_hash(password) })
        db.session.commit()
        return valid
    return valid






