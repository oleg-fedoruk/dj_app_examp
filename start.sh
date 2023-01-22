#!/usr/bin/env bash

python manage.py migrate
#python manage.py uploaddata
python manage.py runserver
#docker-compose down -v
#docker-compose build
#docker-compose up --remove-orphans -d
#sleep 3
#docker exec -it social_net_back python manage.py migrate
#docker exec -it social_net_back python manage.py uploaddata
