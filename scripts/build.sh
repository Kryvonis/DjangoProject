#!/usr/bin/env bash

sudo mkdir venv
virtualenv -p python3 venv
. $(pwd)/venv/bin/activate
pip install -r $(pwd)/requirements.txt
cd ..
cp /src/settings/local.sample.py /srv/www/IgoStories/igostories/settings/local.py
python manage.py makemigrations
python manage.py migrate
sh scripts/run.sh