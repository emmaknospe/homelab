# Use the official Python image as the base image
FROM python:3.11-slim

# Install poetry
RUN pip install --no-cache-dir poetry

# Set the working directory in the container
WORKDIR /app

# Copy the poetry.lock and pyproject.toml files into the container
COPY poetry.lock pyproject.toml ./

# add psycopg2 dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install the Python dependencies (including psycopg2)
RUN poetry install --no-dev --no-root

# Copy the FastAPI application code into the container
COPY . .

# Expose the port that the FastAPI application will run on
EXPOSE 8000

# Set the command to start the FastAPI application
CMD sh -c "poetry run alembic upgrade head && poetry run uvicorn main:app --host 0.0.0.0 --port 8000"