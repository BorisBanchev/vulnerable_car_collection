from sqlalchemy.sql import text
from werkzeug.security import check_password_hash
from db import db
from user import get_user_id
import datetime
def check_user_exists(username):
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    return user

def create_account_valid(username: str, password: str, password2: str):
    user = check_user_exists(username)
    empty_fields = []
    message = ""
    success = False
    if len(username) == 0:
        empty_fields.append("username")
    if len(password) == 0:
        empty_fields.append("password")
    if len(password2) == 0:
        empty_fields.append("password2")
    if len(empty_fields) != 0:
        data = empty_fields, message, success
        return data
    if user:
        message = "Username already exists!"
        data = empty_fields, message, success
        return  data
    if not user and 0 < len(username) <= 20 :
        if password == password2 and 8 <= len(password) <= 20:
            success = True
            message = "Account was created successfully!"
            data = empty_fields, message, success
            return  data
        elif password == password2 and len(password) > 20 or len(password) < 8:
            message = "Invalid password!"
            data = empty_fields, message, success
            return  data
        elif password != password2:
            message = "Passwords don't match!"
            data = empty_fields, message, success
            return  data
    if len(username) > 20:
        message = "Username is too long!"
        data = empty_fields, message, success
        return  data
def login_to_account_valid(username: str, password: str):
    sql = text("SELECT username, password_hash FROM users WHERE username=:username")
    user = db.session.execute(sql, {"username":username}).fetchone()
    empty_fields = []
    message = ""
    success = False
    if len(username) == 0:
        empty_fields.append("username")
    if len(password) == 0:
        empty_fields.append("password")
    if len(empty_fields) != 0:
        data = empty_fields, message, success
        return data
    if not user:
        message = "Invalid username or password!"
        data = empty_fields, message, success
        return data
    if user:
        hash_value = user.password_hash
        if check_password_hash(hash_value, password) and user.username == username:
            success = True
            data = empty_fields, message, success
            return data
        else:
            message = "invalid username or password!"
            data = empty_fields, message, success
            return data
def add_car_valid(brand: str, model: str, prod_year: int, garage_id: int ):
    user_id = get_user_id()
    sql1 = text("""SELECT garages.capacity FROM garages JOIN usergarages ON garages.id = usergarages.garage_id
                             WHERE usergarages.user_id =:user_id AND garages.id=:garage_id""")
    sql2 = text("SELECT COUNT(*) FROM garagecars WHERE garagecars.garage_id=:garage_id")
    if garage_id != "":
        capacity = db.session.execute(sql1, {"user_id":user_id, "garage_id":garage_id}).fetchone()[0]
        cars_in_garage = db.session.execute(sql2, {"garage_id":garage_id}).fetchone()[0]
    current_year = datetime.datetime.today().year
    empty_fields = []
    empty_message = ""
    message = ""
    success = False
    if len(brand) == 0:
        empty_fields.append("brand")
    if len(model) == 0:
        empty_fields.append("model")
    if prod_year == "":
        empty_fields.append("production year")
    if garage_id == "":
        empty_fields.append("garage option")
    if len(empty_fields) == 1:
        empty_message = f"{empty_fields[0]} must be filled!"
        data = empty_fields, empty_message, success
        return data
    if len(empty_fields) > 1:
        for i in range(len(empty_fields)-1):
            empty_message += f"{empty_fields[i]}, "
        empty_message += f"{empty_fields[-1]} must be filled!"
        data = empty_fields, empty_message, success
        return data
    if cars_in_garage < capacity and int(prod_year) < 1886 or int(prod_year) > current_year + 1:
        message = "Invalid production year!"
        data = empty_fields, message, success
        return data
    if cars_in_garage >= capacity: 
        message = "Garage is full!"
        data = empty_fields, message, success
        return data
    if len(brand) > 20 or len(model) > 20:
        message = "The brand or model of the car is too long!"
        data = empty_fields, message, success
        return data
    if cars_in_garage < capacity and 1886 <= int(prod_year) <= current_year + 1 and len(brand) > 0 and len(model) > 0:
        message = "Car added to garage!"
        success = True
        data = empty_fields, message, success
        return data
def create_garage_valid(name: str, capacity: int):
    sql_for_garage = text("SELECT name FROM garages WHERE name=:name")
    garage = db.session.execute(sql_for_garage, {"name":name}).fetchone()
    if garage:
        garage = garage[0]
    else: 
        garage = ""
    empty_fields = []
    empty_message = ""
    message = ""
    success = False
    if len(name) == 0:
        empty_fields.append("name")
    if capacity == "":
        empty_fields.append("capacity")
    if len(empty_fields) == 1:
        empty_message = f"{empty_fields[0]} must be filled!"
        data = empty_fields, empty_message, success
        return data
    if len(empty_fields) > 1:
        empty_message = f"{empty_fields[0]} and {empty_fields[1]} must be filled!"
        data = empty_fields, empty_message, success
        return data
    if capacity > 20 or capacity <= 0:
        message = "Invalid capacity!"
        data = empty_fields, message, success
        return data
    if len(name) > 30 or garage != "":
        message = "Garaga name is too long or it has been already created!"
        data = empty_fields, message, success
        return data
    if len(name) <= 30 and capacity <= 20 and garage == "":
        success = True
        message = "Garage created successfully!"
        data = empty_fields, message, success
        return data
