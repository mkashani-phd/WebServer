FROM python

WORKDIR /code

COPY ./app /code/app

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable

# Run app.py when the container launches
CMD ["python", "app/main.py"]