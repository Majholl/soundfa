#! /bin/bash

set -e 


echo "Running celery...."
celery -A main worker --loglevel=DEBUG --pool=solo