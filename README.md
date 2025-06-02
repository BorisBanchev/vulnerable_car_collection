# Car Collection Web Application

This is a Flask web application with a PostgreSQL database for managing a car collection.

## Features

- Flask backend
- PostgreSQL database
- Dockerized for easy setup
- Schema automatically initialized

---

### Installing and running instructions

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac)
- [Docker Engine & Docker Compose](https://docs.docker.com/engine/install/) (Linux)

---

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/vulnerable_car_collection.git
cd vulnerable_car_collection
```

---

### 2. Start the Application

```bash
docker compose up --build
```

- The first run may take a few minutes as images are built and dependencies installed.
- The database and user are created automatically.
- The schema from `schema.sql` is loaded automatically.

---

### 3. Access the Application

- Open your browser and go to: [http://localhost:5001](http://localhost:5001)

---

## Vulnerabilities chosen from the [OWASP Top 10:2021](https://owasp.org/Top10/)

### Vulnerability 1.

**A01:2021 – Broken Access Control:**
This web application security risk is present in our application as logged in user can open other user's garages without being authorized for that. This can be implemented by modifying the url address from `http://localhost:5001/garage/<logged-user-own-garage-id>` to `http://localhost:5001/garage/target-garage-id` after which we can see other user's garage. This is totally wrongly coded, since we do not check in the garage route if the current logged user owns the garage that needs to be opened.

A solution to the flaw can be obtained with uncommenting the block of code starting from line https://github.com/BorisBanchev/vulnerable_car_collection/blob/main/routes.py#L151

### Vulnerability 2.

**A02:2021 – Cryptographic Failures**
This vulnerability is active in the application since users' passwords are stored in plain text into the database without applying any encryption to the sensitive data. According to the OWASP recommendations it is crucial to apply strong encryption when dealing with sensitive data that belongs to users. In the screenshots folder in the flaw-2 subfolder we can see that passwords are stored in the database as they are writtend from the client.

A solution to the flaw can be obtained with uncommenting the blocks of code starting from lines https://github.com/BorisBanchev/vulnerable_car_collection/blob/main/validate.py#L68 and https://github.com/BorisBanchev/vulnerable_car_collection/blob/main/signup.py#L7

### Vulnerability 3.

**A03:2021 – Injection**
SQL injection vulnerability is really dangerous security leak in the web application since it can lead to database manipulation and in a way that important user data can be stolen, modified or deleted. In our application the user can retrieve the first user's password from the table users by modifying the url from `/garage/<garage-id>` to `/garage/<garage-id> UNION SELECT password_hash FROM users LIMIT 1 OFFSET 0 --` so the user will be able to see the first users password on the garage page on his screen which is totally unaccepted. To prevent SQL injections like this we need to use parameterized sql queries and use text() to prevent these situations of leaking information.

A solution to the flaw can be obtained with uncommenting the block of code starting from line https://github.com/BorisBanchev/vulnerable_car_collection/blob/main/garages.py#L35

### Vulnerability 4.

**A06:2021 – Vulnerable and Outdated Components**
Using outdated and unsecure versions of libraries or components can lead to attackers exploiting vulnerabilities to gain unauthorized access, execute code, compromise data or take control of the system. Currently this flaws is present with the outdated versions of Flask and Flask-SQLAlchemy as their versions are 2.0.0. To prevent this vulnerability, we need to change in the https://github.com/BorisBanchev/vulnerable_car_collection/blob/main/requirements.txt `Flask==2.0.0` to `Flask==3.0.2` and `Flask-SQLAlchemy==2.0.0` to `Flask-SQLAlchemy==3.1.1` and run
`pip3 install Flask==3.0.2 Flask-SQLAlchemy==3.1.1`
