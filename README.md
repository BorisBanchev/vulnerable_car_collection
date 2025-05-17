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
