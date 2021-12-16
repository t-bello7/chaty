# Pull base Image
FROM python:3.7

# Set enviroment variables 
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Set work directory
WORKDIR /chaty
RUN apt-get -y update
RUN adduser appuser --disabled-password
RUN chown -R appuser:appuser /chaty
RUN chmod 775 /chaty

USER appuser

# Install dependencies 
# COPY requirements.txt /chaty/

COPY Pipfile Pipfile.lock /chaty/
RUN pip install pipenv && pipenv install --system


# RUN pip install --upgrade pip \
#     pip install pipenv && pipenv install --deploy --system
#Ask about this pipenv and docker 

# RUN pip install -r requirements.txt

COPY . /chaty/
CMD gunicorn config.wsgi.application --bind 0.0.0.0:$PORT