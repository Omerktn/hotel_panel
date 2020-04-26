from hotelpanel import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


books = db.Table("books",
                 db.Column("customer_tckn", db.Integer, db.ForeignKey("customer.tckn")),
                 db.Column("booking_id", db.Integer, db.ForeignKey("booking.id")))


class Customer(db.Model):
    tckn = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(60))
    sname = db.Column(db.String(60))
    is_inside = db.Column(db.Boolean, default=False, nullable=True)
    card_num = db.Column(db.Integer, nullable=True)
    occ_count = db.Column(db.Integer, nullable=True, default=1)
    phone = db.Column(db.String(20), nullable=True, default="+90")
    bookings = db.relationship("Booking", secondary=books, backref=db.backref("bookers", lazy="dynamic"))

    def __repr__(self):
        return f"User('{self.tckn}', '{self.fname} {self.sname}')"


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=False)
    checkin = db.Column(db.Date)
    checkout = db.Column(db.Date)
    is_online = db.Column(db.Boolean, default=False)
    is_cancelled = db.Column(db.Boolean, default=False)


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tckn = db.Column(db.Integer, unique=True, nullable=True)
    fname = db.Column(db.String(60))
    sname = db.Column(db.String(60), nullable=True)
    position = db.Column(db.String(60))
    salary = db.Column(db.Integer)


class StaffChain(db.Model):
    person = db.Column(db.Integer, db.ForeignKey("staff.id"), primary_key=True)
    superviser = db.Column(db.Integer, db.ForeignKey("staff.id"), primary_key=True)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer, default=1)
    is_full = db.Column(db.Boolean)
    reserv_date = db.Column(db.Date, nullable=True, default=None)
    type = db.Column(db.String, nullable=True, default="standart")


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
