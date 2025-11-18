import logging as lg
from .app import app, db


@app.cli.command()
def syncdb():
    '''Creates all missing tables.'''
    db.create_all()
    lg.warning('Database synchronized!')
