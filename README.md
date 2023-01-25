# Take home assessment


## Development:

### Local development:
#### Config settings:
This project uses dynamic variables that you can set using environment variables or a `.env` file like:

```text
PROJECT_NAME="Take home assessment"
SQLALCHEMY_DATABASE_URI="sqlite:///app.db"
```

####  Main requirements:
- Python3.10
- poetry

Basically you need to setup your poetry environment:

```shell
poetry install
poetry shell
```

Then, you have to create / migrate the database to the actual state:

```shell
alembic upgrade head 
```

And lastly you can run the `manage.py` script:
```shell
python manage.py
```

### Docker development:

For development using docker you will need both docker and docker-compose

```shell
docker-compose up
```

this will fire up everything
