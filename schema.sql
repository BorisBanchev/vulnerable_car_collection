DROP TABLE IF EXISTS garages CASCADE;
DROP TABLE IF EXISTS cars CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS garagecars CASCADE;
DROP TABLE IF EXISTS usercars CASCADE;
DROP TABLE IF EXISTS usergarages CASCADE;


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT
);

CREATE TABLE garages (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    capacity INTEGER NOT NULL
);

CREATE TABLE cars (
    id SERIAL PRIMARY KEY,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    prod_year INTEGER NOT NULL
);  

CREATE TABLE garagecars (
    id SERIAL PRIMARY KEY,
    garage_id INTEGER,
    FOREIGN KEY (garage_id) REFERENCES garages(id) ON DELETE CASCADE,
    car_id INTEGER, 
    FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE CASCADE
);  

CREATE TABLE usercars (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    car_id INTEGER, 
    FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE CASCADE
);  

CREATE TABLE usergarages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    garage_id INTEGER,
    FOREIGN KEY (garage_id) REFERENCES garages(id) ON DELETE CASCADE
);  

