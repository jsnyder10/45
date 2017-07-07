#!flask/bin/python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path
db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,
                        api.version(SQLALCHEMY_MIGRATE_REPO))

from app.models import User, Mobility
user = User(username='snyder')
user.email = 'jonathan.snyder.9@us.af.mil'
user.manpower_admin=True
user.hash_password('catcat')
db.session.add(user)
# add username to Mobility data base
userM=Mobility(username='snyder')
db.session.add(userM)
# make the user follow him/herself
db.session.add(user.follow(user))
db.session.commit()