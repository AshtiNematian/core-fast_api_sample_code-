FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN apt-get update
RUN apt-get install -y wget unzip libpq-dev
RUN apt-get update
RUN  apt-get install -y unixodbc-dev

RUN chmod +rwx /etc/ssl/openssl.cnf
RUN sed -i 's/TLSv1.2/TLSv1/g' /etc/ssl/openssl.cnf
RUN sed -i 's/SECLEVEL=2/SECLEVEL=1/g' /etc/ssl/openssl.cnf

WORKDIR /app/

# Install dependencies
COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY ./app /app

# Copy the code inside container
COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/app"
