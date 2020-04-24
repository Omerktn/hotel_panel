from hotelpanel.models import Staff, Room, Customer
from sqlalchemy import desc, asc


def get_staff_as_select():
    staff_select = [("none", "- (Yok)")]
    q = Staff.query.all()
    for person in q:
        staff_select.append((str(person.tckn), "{} {}".format(person.fname, person.sname)))
    return staff_select


def get_all_customers():
    return Customer.query.order_by(desc(Customer.is_inside)).all()


def get_all_staff():
    return Staff.query.order_by(asc(Staff.tckn)).all()


def number_of_customer_inside():
    return len(Customer.query.filter_by(is_inside=True).all())


def number_of_online_books():
    num = 0
    custs = Customer.query.filter_by(is_inside=False).all()
    for cust in custs:
        if len(cust.bookings) and cust.bookings[-1].is_online:
            num += 1
    return num


def get_customers_rooms():
    cust_and_room = []
    custs = Customer.query.filter_by(is_inside=True).all()
    for cust in custs:
        cust_and_room.append([cust.fname, cust.sname,
                              Room.query.filter_by(id=cust.bookings[-1].room).first().id])
    return cust_and_room


def get_reserved_customers():
    cust_and_room = []
    custs = Customer.query.filter_by(is_inside=False).all()
    for cust in custs:
        if len(cust.bookings) and cust.bookings[-1].is_online:
            cust_and_room.append([cust.fname, cust.sname,
                                  Room.query.filter_by(id=cust.bookings[-1].room).first().id])
    return cust_and_room


def get_full_rooms():
    return Room.query.filter_by(is_full=True).all()


def get_max_room_number():
    room = Room.query.filter_by(reserv_date=None).order_by(desc(Room.id)).first()
    if room:
        return room.id
    return 1000


def get_min_empty_room_number():
    room = Room.query.filter_by(is_full=0).order_by(asc(Room.id)).first()
    if room:
        return room.id
    return None
