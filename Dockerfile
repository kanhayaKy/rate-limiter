FROM python:3.12-slim

# set work directory
WORKDIR /app

## Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
## Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1
## Don't use virtualenv inside docker
ENV POETRY_VIRTUALENVS_CREATE=false


# Update the package list
RUN apt-get update

# Use poetry for dependencies installation
RUN pip install "poetry==2.1.1"
ENV PATH="${PATH}:/root/.poetry/bin"

# make cache dir for models
RUN mkdir /temp

# install python dependencies
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root --no-interaction --no-cache

# Run Application
EXPOSE 5000
CMD [ "poetry", "run", "python", "-m", "flask", "run", "--host=0.0.0.0" ]
