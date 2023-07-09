sudo mkdir ./config/nginx/ssl

sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ./config/nginx/ssl/nginx.key -out ./config/nginx/ssl/nginx.crt

sudo docker-compose up -d