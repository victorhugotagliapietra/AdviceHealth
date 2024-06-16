## Description

This project is a CRUD to manage clients and their vehicles in a city. The application is built with Flask and SQLAlchemy and uses JWT authentication to protect routes.

## Prerequisites

- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Python3](https://www.python.org/downloads/)
- [PIP3](https://www.python.org/downloads/)

## Step-by-Step Guide

### 1. Clone the Repository

Clone the project repository from GitHub:

```sh
git clone https://github.com/victorhugotagliapietra/AdviceHealth.git
cd AdviceHealth
```

### 2. Build DataBase image

1. Add your postgres database credentials in the **config.py** file
2. Run the SQL command below in your postgres database:

```
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TYPE color_enum AS ENUM ('YELLOW', 'BLUE', 'GRAY');
CREATE TYPE model_enum AS ENUM ('HATCH', 'SEDAN', 'CONVERTIBLE');
CREATE TABLE Clients (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  name VARCHAR(255) NOT null,
  sales_opportunity BOOLEAN DEFAULT TRUE
);
CREATE TABLE Vehicles (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  color color_enum NOT NULL,
  model model_enum NOT NULL,
  client_id UUID REFERENCES Clients(id) ON DELETE cascade not NULL
);
CREATE TABLE users (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL
);
```

### 3. Build and Run the Docker Containers

Run the following command to build and start the containers:

```sh
sudo docker-compose up --build
```

### 4. Run Automated Tests

To run the automated tests, open a new terminal and execute:

```sh
docker exec -it <container_name> pytest
```
