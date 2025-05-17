from sqlalchemy.sql import text
from flask import session
from db import db
def get_user_id():
    sql_to_get_user_id = text("SELECT id from users WHERE username=:username")
    user_id = db.session.execute(sql_to_get_user_id, {"username":session["username"]}).fetchone()[0]
    return user_id
