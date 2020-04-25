from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

from hotelpanel import db
from hotelpanel.models import Room, Customer, Booking
from random import randint
import datetime

fnames = ['Can', 'Ahmet', 'Emre', 'Abdullah', 'Ömer', 'Doğaç', 'Günel', "Zeynep"]
snames = ['Güzel', 'Eldenk', 'Yılmaz', 'Toprak', 'Kurttekin', 'Talayhan', 'Eyüp', 'Daniş']

custlist = []

for i in range(len(fnames)):
    cust = Customer(tckn=int(str(i)*11), fname=fnames[i], sname=snames[i],
                    is_inside=False, card_num=randint(10000, 999999),
                    occ_count=randint(1, 3), phone="+905388705742")
    custlist.append(cust)
    db.session.add(cust)

for rm_num in range(1001, 1095):
    new_room = Room(id=rm_num, capacity=2, is_full=False, reserv_date=None)
    db.session.add(new_room)

for idx, cust in enumerate(custlist[:7]):
    book = Booking(room=1001+idx, checkin=datetime.date.today(), checkout=datetime.date.today(),
                   is_online=False, is_cancelled=False)

    Room.query.filter_by(id=1001+idx).first().is_full = True
    cust.is_inside = True
    cust.occ_count += 1

    db.session.add(book)
    book.bookers.append(cust)


db.session.commit()
