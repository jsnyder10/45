from flask import Flask
from flask_alchemydumps import AlchemyDumps, AlchemyDumpsCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

import os
basedir = os.path.abspath(os.path.dirname(__file__))


# init Flask
app = Flask(__name__)

#SQL Alchemy Database config location
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'app.db') +
                               '?check_same_thread=False')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


# init SQLAlchemy and Flask-Script
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = Manager(app)

@manager.command
def hello():
    print "hello"

# init Alchemy Dumps
alchemydumps = AlchemyDumps(app, db)
manager.add_command('alchemydumps', AlchemyDumpsCommand)

if __name__ == "__main__":
    manager.run()