# Setting up Docker

## Installation (for windows)

install Docker desktop - https://docs.docker.com/desktop/install/windows-install/

## Building containers from docker compose

**Ensure you are in the root project directory and the env file is in the project root directory**

### Building development container stack

run the command `docker-compose up`

## Exiting Docker

if using docker desktop you can simply click stop running containers for "app"
if using docker was initialised using a CMD then press **Ctrl + C** or press twice to force close **Ctrl + C , Ctrl + C**

# Setting up the python enviornment (Windows setup)

install python 3.11.4 or the latest version https://www.python.org/downloads/
cd into the root project directory

Run the following commands to create a virtual python enviornment for this project, and upgrade pip

- `python -m venv env`
- `python.exe -m pip install --upgrade pip`

## Activating the virtual python enviornment

`cd venv/scripts && activate && cd..\..`

### If the above command fails then try it separately

- `cd venv/scripts`
- `activate`
- `cd..\..`

## Installing project dependencies

`pip install -r requirements.txt`

## Uninstalling project dependencies (forced)

`pip uninstall -y -r requirements.txt`

## Save project dependencies

`pip freeze > requirements.txt`

# Testing
From the project root directory run the commands `cd src`

# Running unit tests
Run unittests `python -m unittest discover -s tests -p test_*.py`

# Future Work (To be completed) ✨

### Building a local development container stack ()
run the command ```docker-compose -f docker-compose-local.yml up -d```

### Building test container stack
run the command  ```docker-compose -f docker-compose-test.yml -p test up -d```
delete test container ```docker-compose -f docker-compose-test.yml -p test down --volumes```


# Database migrations (Docker)

To begin run the docker containers.

## Creating a migration

To create a new migration use the below command. `docker-compose exec app alembic revision --autogenerate -m "New Migration"`.
<br>You may use a custom migration name instead of "New Migration"

## Running a migration

To run the migration you can use this command. `docker-compose exec app alembic upgrade head`
<br> **You should always check your migration file before running it**

## Reverting a migration

To revert a migration you can use this command. `docker-compose exec app alembic downgrade -1`

### Finding the migration file

From the src go into the db/alembic/versions your new migration will be located here.

# SwaggerDocs

To access the swagger docs you will need to run the project and go to the following url http://localhost:8000/docs

## Database Connection via IDE

To connect to the database via an IDE you will need to uncomment the 2nd database url in the .env file and comment out the first one.
Else it will try to connect to the docker container

## Usable Accounts for the sole purpose of testing and for the purpose of the assignment (These will not be real accounts that would be used in a production environment)
Superuser:
- email: super@super.com
- password: super

Admin:
- email: admin@gg.com
- password: admin

User:
- email: normal@gg.com
- password: normal123