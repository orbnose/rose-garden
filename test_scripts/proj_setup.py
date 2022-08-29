"""
This currently DOES NOT WORK - the virtualenv needs to be activated on the same process as the pip install commands, but that ain't currently happening.
It also needs a call to pip to install django in the venv.
"""

import os

DEFAULT_DIR_NAME = 'testLibrary'
DEFAULT_VENV_NAME = 'djangovenv'
DEFAULT_PROJECT_NAME = 'mysite'
DEFAULT_SETTINGS_FILEPATH = os.path.abspath( os.path.dirname(__file__) + '/settings.py' )

def print_command(command):
    print('===========')
    print('Running command: %s' % command)

def make_dir(relDirName=DEFAULT_DIR_NAME):
    make_command = "mkdir " + relDirName
    print_command(make_command)
    return os.system(make_command)

def enter_dir(relDirName=DEFAULT_DIR_NAME):
    enter_command = "os.chdir(" + relDirName + ")"
    print_command(enter_command)
    os.chdir(relDirName)
    curDir = os.getcwd()
    print("Current working directory is %s" % curDir)

def make_venv(venvName=DEFAULT_VENV_NAME):
    venv_command = "python -m venv " + venvName
    print_command(venv_command)
    return os.system(venv_command)

def activate_venv(venvName=DEFAULT_VENV_NAME):
    command = ". ./ " + venvName + "/bin/activate"
    print_command(command)
    return os.system(command)

def install_rose_garden():
    command = "python -m pip install git+https://github.com/orbnose/rose-garden#egg=rose-garden"
    print_command(command)
    return os.system(command)

def create_django_project(projName=DEFAULT_PROJECT_NAME):
    command = "django-admin startproject " + projName
    print_command(command)
    return os.system(command)

def delete_settings(projName=DEFAULT_PROJECT_NAME):
    command = "rm " + projName + "/" + projName + "/settings.py"
    print_command(command)
    return os.system(command)

def replace_settings(filePath=DEFAULT_SETTINGS_FILEPATH, projName=DEFAULT_PROJECT_NAME):
    escaped_filepath = '"' + filePath + '"'
    escaped_projpath = '"' + projName + "/" + projName + '/settings.py' + '"'
    command = 'cp ' + escaped_filepath  + ' ' + escaped_projpath
    print_command(command)
    return os.system(command)

def make_migrations(projName=DEFAULT_PROJECT_NAME):
    command = "python " + projName + "/manage.py makemigrations rosegarden"
    print_command(command)
    return os.system(command)

def migrate(projName=DEFAULT_PROJECT_NAME):
    command = "python " + projName + "/manage.py migrate"
    print_command(command)
    return os.system(command)

def set_up_test_project(relDirName=DEFAULT_DIR_NAME):
    command_list = [
        make_dir,
        enter_dir,
        make_venv,
        activate_venv,
        install_rose_garden,
        create_django_project,
        delete_settings,
        replace_settings,
        make_migrations,
        migrate,
    ]

    problem=False
    for command in command_list:
        if command(): #The shell will return a non-zero value for any command with an error
            problem = True
            break

    if problem:
        os.chdir('../')
        print("======================")
        os.system('echo "\e[1;31mFAILURE:There was a problem setting up the test environment."')
    else:
        print("======================")
        print("Django test setup is complete!")

if __name__ == '__main__':
    set_up_test_project()