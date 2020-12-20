FROM python:3.7-alpine

# Create app directory
WORKDIR /code

# Install gcc and other dependencies
RUN apk add --no-cache gcc musl-dev linux-headers

# Install python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Container is listening on port 5000
EXPOSE 5000

# Bundle app source
COPY . .

CMD ["flask", "run"]n