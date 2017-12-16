#!/usr/bin/env python3


"""
django-markdown-blog installer.
"""


from subprocess import call
import getpass
import os


COMMANDS = [
    "virtualenv -p python3 venv",
    "source venv/bin/activate",
    "pip install -r requirements.txt",
    "python manage.py migrate",
    "python manage.py createsuperuser",
    "sed -i \'s/ALLOWED_HOST = []/ALLOWED_HOST = [\"{0}.pythonanywhere.com\"]\'".format(
        getpass.getuser()
    )
]

COLOR_DESCRIPTION = "\033[1m\033[96m"
COMMAND_DESCRIPTION = [
    "creating virtualenv for this blog...",
    "activating virtualenv...",
    "installing deps...",
    "migrating blog...",
    "creating superuser. you will be asked superuser name and password."
]

HOME_DIR = os.path.expanduser("~")
WSGI_FILE = '''import os
import sys

path = "{0}"
if path not in sys.path:
    sys.path.append(path)

os.environ[\'DJANGO_SETTINGS_MODULE\'] = \'mysite.settings\'

from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler
application = StaticFilesHandler(get_wsgi_application())'''

for description, command in zip(COMMAND_DESCRIPTION, COMMANDS):
    print(COLOR_DESCRIPTION + description)
    call(command.split())

print(COLOR_DESCRIPTION + "updating wsgi file...")
with open("/var/www/{0}_pythonanywhere_com_wsgi.py", "w") as f:
    f.write(WSGI_FILE.format(HOME_DIR + "/django-markdown-blog"))

print(COLOR_DESCRIPTION + "use this when you are setting web in pythonanywhere.")
print("source code: {0}".format(HOME_DIR + "/django-markdown-blog"))
print("working directoty: {0}".format(HOME_DIR))
print("virtualenv: {0}".format(HOME_DIR + "/django-markdown-blog/venv"))
print("/static/ in static: {0}".format(HOME_DIR + "/django-markdown-blog/blog/static"))
