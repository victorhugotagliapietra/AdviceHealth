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

1. Add your postgres database credentials in the **config.py ** file
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

Run the following command to build and start the containers and the project:

```sh
sudo docker-compose up --build
```

### 4. Run Automated Tests

To run the automated tests, open a new terminal and execute:

1. List the running containers to find the container name:

```sh
docker ps
```

2. Locate the container name from the list. It will look something like advicehealth_db_1.

3. Use the container name in the following command:

```sh
docker exec -it <container_name> pytest
```

Replace {container_name} with the actual name of your application container.

### 5. Access the Application

Once the containers are up and running, you can access the application at http://localhost:5000.

### 6. API Endpoints

Below are the API endpoints with methods for testing via Postman.

##### Authentication

- Register: **POST** /auth/register
  Request Body:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

- Login: **POST** /auth/login
  Request Body:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

##### Clients

- Create Client: **POST** /clients
  Request Body:

```json
{
  "name": "Client Name"
}
```

- Get All Clients: **GET** /clients
- Get Client by ID: **GET** /clients/{client_id}
- Update Client: **PUT** /clients/{client_id}
  Request Body:

```json
{
  "name": "Updated Client Name"
}
```

- Delete Client: DELETE /clients/{client_id}

##### Vehicles

- Create Vehicle: **POST** /vehicles
  Request Body:

```json
{
  "color": "YELLOW",
  "model": "HATCH",
  "client_id": "client_id"
}
```

- Get All Vehicles: **GET** /vehicles

- Get Vehicle by ID: **GET** /vehicles/{vehicle_id}

- Update Vehicle: **PUT** /vehicles/{vehicle_id}

Request Body:

```json
{
  "color": "BLUE",
  "model": "SEDAN"
}
```

- Delete Vehicle: DELETE /vehicles/{vehicle_id}

### 7. Using Postman

1. Open Postman and create a new request.
2. Select the HTTP method (GET, POST, PUT, DELETE).
3. Enter the URL for the API endpoint.
4. For endpoints requiring a request body, select Body and raw, then choose JSON from the dropdown.
5. Copy and paste the example request body (as shown above) into the body section.
6. For endpoints requiring authentication, go to the Headers tab and add the Authorization header with the value Bearer {your_jwt_token}.

### 8. JWT Token

After registering and logging in, you will receive a JWT token. Use this token to authenticate your requests by adding it to the Authorization header in Postman as shown below:

```http
Authorization: Bearer <your_jwt_token>
```
