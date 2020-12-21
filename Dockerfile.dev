FROM python:3.8-slim-buster

# Create app directory
WORKDIR /code

# Install python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Container is listening on port 5000
EXPOSE 5000

# Bundle app source
COPY . .

CMD ["flask", "run"]