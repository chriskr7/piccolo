#!/bin/sh
curl -H "Piccolo-App-ID: bulma" -H "Content-Type: application/json" \
-X GET "http://52.74.37.107:7200/v1/app/user" \
-d '{"uid": "chriskr7@gmail.com"}'
