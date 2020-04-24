from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from hotelpanel import db
from hotelpanel.models import Staff
from random import randint

fnames = ["Birol", "Hande", "Ali", "Burham"]
snames = ['Tayşi', 'Akgül', 'Sallanmazer', 'Varol']

custlist = []

for i in range(len(fnames)):
    for j in range(len(fnames)):
        person = Staff(tckn=randint(100000000, 99999999999), fname=fnames[i], sname=snames[j],
                       position="service", salary=randint(2, 10)*10000000)
        db.session.add(person)

db.session.commit()
