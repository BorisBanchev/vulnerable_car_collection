from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask import session
from user import get_user_id
from validate import create_garage_valid
from db import db
import datetime

def create_garage_(name: str, capacity: int):
    sql1 = text("INSERT INTO garages (name, capacity) VALUES (:name, :capacity) RETURNING id")
    sql2 = text("SELECT id from users WHERE username=:username")
    sql3 = text("INSERT INTO usergarages (user_id, garage_id) VALUES (:user_id, :garage_id)")
    data = create_garage_valid(name, capacity)
    if data[2]:
        garage_id = db.session.execute(sql1, {"name":name, "capacity":capacity}).fetchone()[0]
        db.session.commit()
        user_id = get_user_id()
        db.session.execute(sql3, {"user_id":user_id, "garage_id":garage_id})
        db.session.commit()
        return data
    return data
def remove_garage_(garage_id: int):
    sql1 = text("DELETE from garages where garages.id=:garage_id")
    sql2 = text("""SELECT cars.id from cars join garagecars on cars.id = garagecars.car_id 
                                  join garages on garages.id = garagecars.garage_id where garagecars.garage_id=:garage_id""")
    sql3 = text("DELETE from cars where cars.id=:car_id")
    cars = db.session.execute(sql2, {"garage_id":garage_id}).fetchall()
    for car_id in cars:
        db.session.execute(sql3, {"car_id":car_id[0]})
        db.session.commit()

    db.session.execute(sql1, {"garage_id":garage_id})
    db.session.commit()
def open_garage(garage_id: int):
    sql1 = text("SELECT garages.name from garages where id=:garage_id")
    sql2 = text("""SELECT cars.id, cars.brand, cars.model, cars.prod_year from cars join garagecars on cars.id = garagecars.car_id
                 join garages on garages.id = garagecars.garage_id where garagecars.garage_id=:garage_id""")
    garage_name = db.session.execute(sql1, {"garage_id":garage_id}).fetchone()[0]
    cars = db.session.execute(sql2, {"garage_id":garage_id}).fetchall()
    return (garage_name, cars)

def cars_inside(garage_id: int):
    sql = text("SELECT COALESCE(COUNT(*), 0) FROM garagecars WHERE garage_id =:garage_id")
    cars = db.session.execute(sql, {"garage_id":garage_id}).fetchone()[0]
    return cars

