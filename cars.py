from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask import session
from db import db
from user import get_user_id
from validate import add_car_valid

def remove_car_(car_id: int):
    sql = text("DELETE from cars where cars.id=:car_id")
    db.session.execute(sql, {"car_id":car_id})
    db.session.commit()

def add_car_(brand: str, model: str, prod_year: int, garage_id: int ):
    sql1 = text("INSERT INTO cars (brand, model, prod_year) VALUES (:brand, :model, :prod_year) RETURNING id")
    sql2 = text("INSERT INTO garagecars (garage_id, car_id) VALUES (:garage_id, :car_id)")
    user_id = get_user_id()
    if prod_year != "" and garage_id != "":
        car_id = db.session.execute(sql1, {"brand":brand, "model":model, "prod_year":prod_year }).fetchone()[0]
        db.session.commit()
    sql3 = text("INSERT INTO usercars (user_id, car_id) VALUES (:user_id, :car_id)")
    data = add_car_valid(brand, model, prod_year, garage_id)
    if data[2]:
        db.session.execute(sql2,{"garage_id":garage_id,"car_id":car_id})
        db.session.commit()
        db.session.execute(sql3,{"user_id":user_id, "car_id":car_id})
        db.session.commit()
        return data
    return data
