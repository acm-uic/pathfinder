FROM python:2

RUN apt-get update && apt-get install -y apache2

RUN pip install Pillow==2.0

WORKDIR /root

ADD --chown=www-data:www-data ./var-www /var/www
ADD ./etc-apache2-sites-enabled-000-default.conf /etc/apache2/sites-enabled/000-default.conf

RUN a2enmod cgi

EXPOSE 80

USER root

CMD apachectl -D FOREGROUND
