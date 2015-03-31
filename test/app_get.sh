#!/bin/sh
curl -H "Piccolo-App-ID: bulma" \
    -X GET "http://localhost:7200/v1/app"
