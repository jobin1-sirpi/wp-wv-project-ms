# WP-WV-PROJECT-MS

_MicroService to handle Project based functionalities in WindVista V2_

## Project Description

This service provides a robust backend API for managing projects for WindVista V2. Built with FastAPI, it ensures high performance, scalability, and security. The project is structured using Poetry for dependency management and script configuration, enabling seamless development and deployment.

## Requirements

- Python 3.12 or higher
- Poetry >=1.8.0 or <=1.8.4 for dependency management

## Installation

1. **Clone the repository:**

   ```shell
   git clone https://github.com/sirpi-in/wp-wv-project-ms.git
   cd wp-wv-project-ms/
   ```

2. **Install Poetry:**

   If you don't have Poetry installed, you can install it using pip:

   ```cmd
   pip install poetry==1.8.4
   ```

   Alternatively, you can refer to the [Poetry installation documentation](https://python-poetry.org/docs/#installation) for more installation options.

3. **Install project dependencies:**

   ```sh
   poetry install
   ```

## Running the Project

### Running in Development Mode

To run the project in development mode, which include features such as hot-reloading, use the following command:

```sh
poetry run dev
```

### Running with Docker

To run the project using Docker, follow these steps:

> `Note:` If you are new to Docker, refer to the [official Docker documentation](https://docs.docker.com/get-started/) for a guide on setting up Docker on your machine.

1. **Build the project with Poetry:**

   ```sh
   poetry build
   ```

   This command will create a **distribution(./dist)** package of the project.

2. **Build the Docker image:**

   ```sh
   docker build -t wp-wv-project-ms .
   ```

3. **Run API**

   a. **Run the Docker container:**

   ```sh
   docker run -p 5000:5000 --name wp-wv-project-ms-container wp-wv-project-ms sh -c api
   ```

   This command will start the container and map port 5000 of the container to port 5000 on your host machine.

### Accessing the API

You can now access the API by navigating to http://localhost:5000 in your web browser or using tools like **[ThunderClient](https://docs.thunderclient.com/) / [Postman](https://learning.postman.com/docs/introduction/overview/)** or you can access **Swagger/Redoc** API Documentation on **_/docs_** or **_/redoc_** endpoints.

## Authors

- Muzaffar Shaikh - [muzaffar@sirpi.io](mailto:"Muzaffar%20Shaikh"<muzaffar@sirpi.io>)
