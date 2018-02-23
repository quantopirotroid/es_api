#!/bin/bash

set -e
cd $(dirname "$0")

source .env
SSL_DIR=$NGINX_DIR/conf.d/ssl

for dir in "$NGINX_DIR" "$SSL_DIR" "$ES_DATA_DIR"; do
    test -d $dir && echo "$dir already exist"
done

mkdir -p {$NGINX_DIR,$SSL_DIR,$ES_DATA_DIR}

if [[ "yes" == $USE_EXISTENT_CERTIFICATE ]]; then
    cp {$CRT_PATH,$KEY_PATH} $SSL_DIR
else
    CRT_PATH=$SSL_DIR/nginx_es_api_ss.crt
    KEY_PATH=$SSL_DIR/nginx_es_api_ss.key
    openssl req -x509 -nodes -days $CRT_EXPIRE -batch -newkey rsa:2048 -keyout $KEY_PATH -out $CRT_PATH
fi

cp nginx.conf.default nginx.conf

CRT_PATH=/etc/nginx/conf.d/ssl/$(echo $CRT_PATH | awk -F/ '{print $NF}')
KEY_PATH=/etc/nginx/conf.d/ssl/$(echo $KEY_PATH | awk -F/ '{print $NF}')

sed -i "s/%CRT_PATH%/$(echo $CRT_PATH | sed 's/\//\\\//g')/" nginx.conf
sed -i "s/%KEY_PATH%/$(echo $KEY_PATH | sed 's/\//\\\//g')/" nginx.conf
sed -i "s/%API_SERVER_NAME%/$API_SERVER_NAME/" nginx.conf
sed -i "s/%API_PORT%/$API_PORT/" nginx.conf

mv nginx.conf $NGINX_DIR
docker-compose up -d
