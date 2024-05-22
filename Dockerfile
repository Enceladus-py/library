FROM python:3.12-slim-bullseye

# Set the working directory in docker
WORKDIR /app

# For virtual environment
RUN python3 -m venv /opt/venv

# Docker will detect it and use the cache 
COPY ./requirements.txt /app/requirements.txt

# Install dependencies in venv
RUN . /opt/venv/bin/activate && pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

# Run the application
CMD . /opt/venv/bin/activate && fastapi run app/main.py --port 80
