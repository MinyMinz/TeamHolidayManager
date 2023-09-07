# TeamHolidayManager
 Fast API project to manage holiday requests using a postgres database.
 Also manages a list of teams, users within their teams and their application privileges.

# Setting up Docker

## Installation (for windows)
install Docker desktop - https://docs.docker.com/desktop/install/windows-install/

## Building containers from docker compose 
**Ensure you are in the root project directory and the env file is in the project root directory**
### Building development container stack
run the command ```docker-compose up```

## Exiting Docker
if using docker desktop you can simply click stop running containers for "app"
if using docker was initialised using a CMD then press **Ctrl + C** or press twice to force close  **Ctrl + C , Ctrl + C**

# Setting up the python enviornment (Windows setup)
install python 3.11.4 or the latest version https://www.python.org/downloads/
cd into the root project directory

Run the following commands to create a virtual python enviornment for this project, and upgrade pip
- ```python -m venv env```
- ```python.exe -m pip install --upgrade pip```

## Activating the virtual python enviornment
```cd venv/scripts && activate && cd..\..```

### If the above command fails then try it separately 
- ```cd venv/scripts```
- ```activate```
- ```cd..\..```

## Installing project dependencies
```pip install -r requirements.txt```

## Uninstalling project dependencies (forced)
```pip uninstall -y -r requirements.txt```

## Save project dependencies
```pip freeze > requirements.txt```

# Testing

From the project root directory run the commands ```cd src```

Run tests without coverage ```python -m unittest discover -s tests -p test_*.py```

# Database migrations (need to verify this can be done via docker)

To begin run the docker containers.

## Creating a migration
To create a new migration use the below command. ```docker-compose exec app alembic revision --autogenerate -m "New Migration"```.
<br>You may use a custom migration name instead of "New Migration"

## Inserting data into the database
To insert data into the database you can add the below code to the migration file.
Insert data into database add the following to the upgrade function in the migration script
<br>**You should always check your migration file before running it**

    op.bulk_insert(
        sa.table('Roles', sa.column('name'), sa.column('description')),
        [
            {'name': 'SuperAdmin', 'description': 'This is a SuperAdmin user'},
            {'name': 'Admin', 'description': 'This is an Admin user'},
            {'name': 'User', 'description': 'This is a Standard user'},
        ],
    )

    op.bulk_insert(
        sa.table('Teams', sa.column('name'), sa.column('description')),
        [
            {'name': 'Team GG', 'description': 'This is Team GG'},
            {'name': 'Team Matrix', 'description': 'This is Team Matrix'},
            {'name': 'Team Mamba', 'description': 'This is Team Mamba'},
        ],
    )

    op.bulk_insert(
        sa.table('Users', sa.column('full_name'), sa.column('email'), sa.column('password'), sa.column('team_name'), sa.column('role_name')),
        [
            {'full_name': 'SuperAdmin', 'email': 'super@super.com', 'password': 'super', 'team_name': 'Team GG', 'role_name': 'SuperAdmin'},
            {'full_name': 'Admin', 'email': 'admin@GG.com', 'password': 'admin', 'team_name': 'Team Matrix', 'role_name': 'Admin'},
            {'full_name': 'User', 'email': 'normal@gg.com', 'password': '123', 'team_name': 'Team Matrix', 'role_name': 'User'},
        ]
    )

## Running a migration
To run the migration you can use this command. ```docker-compose exec app alembic upgrade head``` 
<br> **You should always check your migration file before running it**

## Reverting a migration
To revert a migration you can use this command. ```docker-compose exec app alembic downgrade -1```

### Finding the migration file
From the src go into the db/alembic/versions your new migration will be located here. 

# SwaggerDocs
To access the swagger docs you will need to run the project and go to the following url http://localhost:8000/docs

