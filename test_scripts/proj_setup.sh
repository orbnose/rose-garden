#!/bin/bash

#setup for copying pre-made Django settings.py from script directory
scriptdir="$( dirname -- "$BASH_SOURCE"; )";
settingsdir="${scriptdir}/settings.py"

#save the parent directory of the test project
ROSEGARDEN_TEST_PARENT_DIR=$(pwd)
parentdirfile="/tmp/rg_test_parent_dir.dat"
echo ${ROSEGARDEN_TEST_PARENT_DIR} >"$parentdirfile"

#make the test directory, create venv, install django and rosegarden, make migrations
mkdir rgTestLibrary
cd rgTestLibrary
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
