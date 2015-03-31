#!/bin/sh
curl -H "Piccolo-App-ID: bulma" -H "Content-Type: application/json" \
-X POST "http://52.74.37.107:7200/v1/app/user" \
-d '{"uid": "chriskr7@gmail.com", "dev_token": "67B0F699BAE82FD290B224196CE4E3443AF6434D857D431AE7DB9075A9B7C134", "os_type": "A"}'
#-d '{"uid": "chriskr7@gmail.com",
#"dev_token": "APA91bFoWv6eQXUQyl1x8xEehRvvqmV_VdzE0AsLrF03lb3qa75mWO8_yMeQ7373ezj1oN8fyAUDi8s4Kolbe4p31HvfQ3uuvSFs3yHuJY5e_XiP5bzgcnslUCTqrnyZWUVzfMT0uYIlp-8EZ4PJDm8RJVMrMMFqgcPjr9tZJQhLwQpqHPd6D58", "os_type":"A"}'
