FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
&& apt-get install gcc --no-install-recommends -y \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install poetry
COPY poetry.lock pyproject.toml /app/
RUN poetry export -f requirements.txt | pip install --no-cache-dir -r /dev/stdin

COPY . /app
COPY ./docker/entrypoint.sh /app/
RUN chmod a+x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "manage.py"]
