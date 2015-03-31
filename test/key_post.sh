#!/bin/sh
curl -H "Piccolo-App-ID: bulma" -H "Content-Type: application/json" \
-X POST "http://localhost:7200/v1/app/key" \
-d '{
    "gcm_key": "AIzaSyAfhHymLOvcByBHYoMZtmFO9QA6KQvGkC0",
    "ios_key": "/home/ubuntu/snmp/cert/ios_key.pem",
    "ios_cert":"/home/ubuntu/snmp/cert/ios_cert.pem"
    }'
