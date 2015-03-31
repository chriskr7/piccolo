#!/bin/sh
curl -H "Piccolo-App-ID: test" -H "Content-Type: application/json" \
-X PUT -d '{"status": "__RUN__"}' "http://localhost:7200/v1/app"
