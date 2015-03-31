#!/bin/sh
curl -H "Piccolo-App-ID: test" \
-X DELETE "http://localhost:7200/v1/app/key"
