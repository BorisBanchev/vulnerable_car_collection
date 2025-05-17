from app import app
from jinja2 import Environment
import secrets
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask import render_template, redirect, request, session, url_for
from os import getenv
from signup import create_account
from login import login_to_account
from garages import create_garage_, remove_garage_, open_garage, cars_inside
from cars import add_car_, remove_car_
from db import db

app.secret_key = getenv("SECRET_KEY")
app.jinja_env.globals.update(zip=zip)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        data = create_account(username, password, password2)
        empty_fields = data[0]
        message = data[1]
        success = data[2]
        if len(empty_fields) != 0:
            return render_template(
                "signup.html",
                message="username or password must be filled!",
                success=success,
                username=None,
            )
        return render_template(
            "signup.html", message=message, success=success, username=username
        )
    if request.method == "GET":
        return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        data = login_to_account(username, password)
        empty_fields = data[0]
        message = data[1]
        success = data[2]
        if len(empty_fields) != 0:
            return render_template(
                "login.html",
                message="username or password must be filled!",
                success=success,
                username=None,
            ) 
        elif success:
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/profile")
        else:
            return render_template(
                "login.html", message=message, success=success, username=username
            )
    if request.method == "GET":
        return render_template("login.html")


@app.route("/logout")
def logout():
    del session["username"]
    del session["csrf_token"]
    return redirect("/")


@app.route("/profile")
def profile():
    try:
        if session["username"]:
            sql1 = text("SELECT id from users WHERE username=:username")
            sql2 = text(
                """select usergarages.id, garages.name, garages.capacity from users join usergarages on users.id = usergarages.user_id 
                        join garages on garages.id = usergarages.garage_id where users.id=:user_id"""
            )
            user_id = db.session.execute(
                sql1, {"username": session["username"]}
            ).fetchone()[0]
            garages = db.session.execute(sql2, {"user_id": user_id}).fetchall()
            cars = [cars_inside(garage[0]) for garage in garages]
            return render_template("profile.html", garages=garages, cars=cars)
    except:
        return render_template(
            "error.html", message="You have to be logged in to view car collection!"
        )
        


@app.route("/create_garage", methods=["POST", "GET"])
def create_garage():
    try:
        if session["username"]:
            if request.method == "POST":
                if session["csrf_token"] != request.form["csrf_token"]:
                    abort(403)
                name = request.form["garage_name"]
                capacity = request.form["capacity"]
                if capacity != "":
                    data = create_garage_(name, int(capacity))
                    empty_fields = data[0]
                    message = data[1]
                    success = data[2]
                else:
                    data = create_garage_(name, capacity)
                    empty_fields = data[0]
                    message = data[1]
                    success = data[2]
                return render_template(
                    "create_garage.html",
                    name=name,
                    capacity=capacity,
                    message=message,
                    success=success,
                )
            elif request.method == "GET":
                return render_template("create_garage.html")
    except KeyError:
        return render_template(
            "error.html", message="You have to be logged in to create a garage!"
        )


@app.route("/remove_garage/<int:garage_id>")
def remove_garage(garage_id: int):
    remove_garage_(garage_id)
    return redirect("/profile")


@app.route("/garage/<int:garage_id>")
def garage(garage_id: int):
    try:
        if session["username"]:
            data = open_garage(garage_id)
            if data:
                garage_name = data[0]
                cars = data[1]
                return render_template(
                    "garage.html",
                    garage_name=garage_name,
                    cars=cars,
                    garage_id=garage_id,
                )
    except:
        return render_template(
            "error.html", message="You have to be logged in to see garage!"
        )


@app.route("/add_car", methods=["POST", "GET"])
def add_car():
    try:
        if session["username"]:
            sql1 = text("SELECT id from users WHERE username=:username")
            sql2 = text(
                """select usergarages.id, garages.name, garages.capacity from users join usergarages on users.id = usergarages.user_id 
                        join garages on garages.id = usergarages.garage_id where users.id=:user_id"""
            )
            user_id = db.session.execute(
                sql1, {"username": session["username"]}
            ).fetchone()[0]
            garages = db.session.execute(sql2, {"user_id": user_id}).fetchall()
            if request.method == "GET":
                return render_template("add_car.html", garages=garages)
            if request.method == "POST":
                if session["csrf_token"] != request.form["csrf_token"]:
                    abort(403)
                car_brand = request.form["carbrand"]
                car_model = request.form["carmodel"]
                prod_year = request.form["production_year"]
                garage_id = request.form["garage_id"]
                if prod_year != "" and garage_id != "":
                    data = add_car_(
                        car_brand, car_model, int(prod_year), int(garage_id)
                    )
                    empty_fields = data[0]
                    message = data[1]
                    success = data[2]
                else:
                    data = add_car_(car_brand, car_model, prod_year, garage_id)
                    empty_fields = data[0]
                    message = data[1]
                    success = data[2]
                return render_template(
                    "add_car.html",
                    message=message,
                    success=success,
                    car_brand=car_brand,
                    car_model=car_model,
                    prod_year=prod_year,
                    garages=garages,
                    empty_fields=empty_fields,
                )
    except KeyError:
        return render_template(
            "error.html", message="You have to be logged in to add cars!"
        )


@app.route("/remove_car")
def remove_car():
    garage_id = request.args.get("garage_id")
    car_id = request.args.get("car_id")
    remove_car_(car_id)
    return redirect(url_for("garage", garage_id=garage_id))
