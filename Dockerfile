# FROM directive instructing base image to build upon
FROM python:3.13-slim

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /app/
COPY . /app/

# Sets the local timezone of the Docker image
ENV TZ=America/Detroit
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# This will need some parameters to actually do anything
CMD ["python ./update_accounts.py"]

# Done!
