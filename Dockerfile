# Stage 1: Build Stage
FROM python:3.11-slim-buster AS build

# Install build dependencies for cryptography and Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libffi-dev libssl-dev libjpeg-dev zlib1g-dev

# Stage 2: Runtime Stage
FROM python:3.11-slim-buster

# Copy the installed libraries from the build stage
COPY --from=build /usr/lib/x86_64-linux-gnu /usr/lib/x86_64-linux-gnu
COPY --from=build /usr/lib/x86_64-linux-gnu /usr/lib/x86_64-linux-gnu

# Create a group and user
RUN groupadd -r mygroup && useradd -r -g mygroup myuser

# Set the working directory
WORKDIR /app

# Copy your application code into the container
COPY . /app

# Change the owner of the application directory to the newly created user
RUN chown -R myuser:mygroup /app

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install PostgreSQL client (psql)
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client

# Install any Python dependencies for your application
RUN pip install -r requirements.txt

EXPOSE 8005

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8005"]
