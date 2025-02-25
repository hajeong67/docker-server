# Use the official image as a parent image
FROM ubuntu:jammy

# Update the system
RUN apt-get update && apt-get upgrade -y

# Install Common Software
RUN ln -fs /usr/share/zoneinfo/Asia/Seoul /etc/localtime
RUN apt-get install -y software-properties-common

# Install pip
RUN apt-get install -y python3-pip

# Install geos
RUN apt-get install -y libgeos++-dev

# Install proj
RUN apt-get install -y proj-bin

# Add the Ubuntu GIS PPA
RUN add-apt-repository ppa:ubuntugis/ppa && apt-get update

# Install gdal
RUN apt-get install -y gdal-bin

# install gdal
RUN apt-get install -y libgdal-dev
RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal

# install gdal for python
RUN pip install gdal

# Install gettext
RUN apt-get install -y gettext

# Install postgrsql devel lib
RUN apt-get install -y libpq-dev

# set work directory
WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt

COPY . /app

RUN chmod +x /app/entrypoint.sh