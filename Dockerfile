FROM python:3.12-slim-bullseye

# Set the working directory in docker
WORKDIR /app

# For virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Docker will detect it and use the cache 
COPY app/requirements.txt requirements.txt

# Install dependencies in venv
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the app directory contents into the container at /app
COPY /app .

# Copy also pyproject
COPY pyproject.toml ../

# Install it as a package to ensure abs import works
RUN cd .. && pip install -e .