# Take home assessment


## Development:

### Local development:
#### Config settings:
This project uses dynamic variables that you can set using environment variables or a `.env` file like:

```text
PROJECT_NAME="Take home project local"
SQLALCHEMY_DATABASE_URI="sqlite:///app.db"
TEST_TARGET=remote
REMOTE_ENDPOINT="https://concha-labs-375805.uc.r.appspot.com"
```

####  Main requirements:
- Python3.10
- poetry

Basically you need to set up your poetry environment:

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


## Deployment:
The current server architecture is based on Google AppEngine and SQL Server (PostgreSQL) with an internal VPC for communication

you can refer to the file `app.yml` for the service configuration.

## Testing:
For testing we are using `pytest`, you can install with poetry by running:

```shell
poetry install --with dev
```

After the dependencies are installed, you can run `pytest` to run the current tests

We are currently using a local sqlite database so, don't forget to run `alembic upgrade head` in order to have the most recent database.

### Testing environments:
The tests has a couple of configurations in the `settings.py` file:

- `TEST_TARGET` could be `local` or `remote` and this means if we want to run the tests against the local or a remote server.
- `REMOTE_ENDPOINT` in case the test target is remote we can specify the remote server address that we can use for running the tests.

## Last comments / improvements:

- I just covered the happy path in tests, we need to expand the test scenarios to all the cases and validations.
- The search endpoint uses an approach of multiple SQL `like` (see [here](github.com/soloidx/cnch_assestment/blob/c9df17090d5e50fc546e63d6e470817cde8e9564/project/crud/user.py#L11-L24) ) statements, I would improve this by creating an indexer or at least creating a search field in the table.
- We need a fallback method / endpoint that we can use in test in order to clean the database when all the tests are finished, just in case a test fails and some test data are still in the database.
