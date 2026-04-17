### Setup (in root directory):
Preconditions:
- Clone this repository: git clone https://github.com/Dasha05896/travel_project
- Start Docker Desktop or ensure the Docker service is running

#### Build docker containers
```shell
docker-compose build
```

#### Apply initial migrations
```shell
docker-compose run app python manage.py migrate 
```

#### Run docker-compose
```shell
docker-compose up
```

### Additional commands

### Create superuser for admin panel:
```shell
docker-compose run app python manage.py createsuperuser
```


### General Info

- Docker-compose setup: Demonstrates containerization skills by packaging the Django application for rapid deployment in an isolated environment.
- API Integration: Implemented integration with the Art Institute of Chicago API to validate locations via their external_id before saving.
- Business Logic:
  - Constraints: Enforced a limit of no more than 10 places per travel project. 
  - Automation: Projects are automatically marked as is_completed once all associated places have been marked as visited. 
  - Deletion Validation: Projects cannot be deleted if they contain any places that have already been visited.
