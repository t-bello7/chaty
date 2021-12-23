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
RUN apt-get -y update && apt-get install -y 
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
USER root
RUN chmod -R u+x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]

CMD ["sh", "-c","tail -f /dev/null"]
USER appuser