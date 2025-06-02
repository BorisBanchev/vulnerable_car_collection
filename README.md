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

## Vulnerabilities chosen from the \_[OWASP Top 10:2021](https://owasp.org/Top10/)

### Vulnerability 1.

**A01:2021 – Broken Access Control**
This web application security risk is present in our application as logged in user can open other user's garages without being authorized for that. This can be implemented by modifying the url address from `http://localhost:5001/garage/<logged-user-own-garage-id>` to `http://localhost:5001/garage/target-garage-id` after which we can see other user's garage. This is totally wrongly coded, since we do not check in the garage route if the current logged user owns the garage that needs to be opened.

A solution to the flaw can be obtained with uncommenting the block of code starting from line https://github.com/BorisBanchev/vulnerable_car_collection/blob/main/routes.py#L150
