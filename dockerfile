#Deriving the latest base image
FROM python:latest


#Labels as key value pair
LABEL Maintainer="vanseforge"


WORKDIR /usr/app/rhino

# Install required packages
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install websockets
RUN pip install requests
RUN pip install python-openhab
RUN pip install pydub
RUN pip install xmltodict
RUN pip install python-i18n[YAML]
RUN pip install pyyaml

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
RUN apt-get install -y locales locales-all

#Copy all files in the container
COPY . .

RUN pip install -e .

# Run python program
CMD [ "python", "main.py"]