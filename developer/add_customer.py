from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from hotelpanel import db
from hotelpanel.models import *
from random import randint

fnames = ['Can', 'Ahmet', 'Emre', 'Abdullah', 'Ömer', 'Doğaç', 'Günel', "Zeynep"]
snames = ['Güzel', 'Eldenk', 'Yılmaz', 'Toprak', 'Kurttekin', 'Talayhan', 'Eyüp', 'Daniş']

for i in range(len(fnames)):
    cust = Customer(tckn=int(str(i)*11), fname=fnames[i], sname=snames[i],
                    is_inside=False, card_num=randint(10000, 999999), occ_count=randint(1, 3))
    db.session.add(cust)

db.session.commit()
