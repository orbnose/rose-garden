#!/bin/bash

scriptdir="$( dirname -- "$BASH_SOURCE"; )";
settingsdir="${scriptdir}/settings.py"

mkdir testLibrary
cd testLibrary
python -m venv djangovenv
source djangovenv/bin/activate
python -m pip install django
python -m pip install git+https://github.com/orbnose/rose-garden#egg=rose-garden
django-admin startproject mysite
rm mysite/mysite/settings.py
cp "${settingsdir}" "mysite/mysite/settings.py"
cd mysite
python manage.py makemigrations rosegarden
python manage.py migrate