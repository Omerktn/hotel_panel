from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda: 0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from hotelpanel import db, bcrypt
from hotelpanel.models import *

db.create_all()

hashed_pw = bcrypt.generate_password_hash("123").decode("utf-8")
user = User(username="admin", email="admin@adastr.com", password=hashed_pw)
db.session.add(user)
db.session.commit()
