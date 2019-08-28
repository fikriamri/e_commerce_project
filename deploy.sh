#!/bin/bash
sudo docker stop backend
sudo docker rm backend
sudo docker rmi fikriamri/e-commerce-backend:v.1
sudo docker run -d -p 5020:5020 --name backend fikriamri/e-commerce-backend:v.1