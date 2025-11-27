#>>>import random, string, os
#>>>"".join([random.choice(string.printable) for _ in os.urandom(24) ] )

import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'monApp.db')
DEBUG = True
TEMPLATES_AUTO_RELOAD = True
SECRET_KEY = '?IhC;r5ZWv=sNK\x0c0:<J"-[@e'
