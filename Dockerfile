# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
COPY entrypoint.sh .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

RUN pip install -r requirements.txt
RUN ["chmod", "+x", "entrypoint.sh"]

EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE=config.settings.dev

ENTRYPOINT ["sh", "entrypoint.sh" ]