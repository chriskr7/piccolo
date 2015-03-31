#!/bin/sh
curl -H "Piccolo-App-ID: test" -H "Content-Type: application/json" \
-X PUT "http://localhost:7200/v1/app/user" \
-d '{"uid": "chriskr7@gmail.com", "dev_token": "003007", "os_type": "A"}'
