#!/bin/bash

docker-compose down -v
docker-compose up -d --build
# docker exec realsensetrainer_rst_1 /rst/main.prod.sh