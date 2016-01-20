#!/bin/bash

echo "Starting App Engine"
~/appenginesdk/google_appengine/dev_appserver.py --log_level=debug --skip_sdk_update_check=yes --host=0.0.0.0 --port=80 /var/www/
