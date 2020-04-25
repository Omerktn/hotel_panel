from random import randint

from flask import flash, redirect, render_template, request, url_for

from flask_login import current_user, login_user, logout_user
from hotelpanel import APP, bcrypt, db
from hotelpanel.forms import (AddRoomForm, AddStaffForm, CustomerBookingForm,
                              CustomerInForm, CustomerOutForm, LoginForm,
                              RegistrationForm, CustomerCancelForm)
from hotelpanel.methods import (get_customers_rooms, get_max_room_number,
                                get_min_empty_room_number,
                                number_of_customer_inside, get_reserved_customers,
                                number_of_online_books, get_all_staff, get_all_customers)
from hotelpanel.models import Booking, Customer, Room, Staff, User

posts = [
    {"title": "Domatesin faydaları!",
     "author": "omerktn",
     "content": "Bol vitamin-C içerir",
     "date_posted": "12 Nisan, 2020"},
    {"title": "Otel açılıyor!",
     "author": "admin",
     "content": "Uludağ Vadi Otelleri yakında hizmetinizde.",
     "date_posted": "09 Mayıs, 2020"}
]


@APP.route("/staffinfo", methods=['GET', 'POST'])
def staff_info():
    if not current_user.is_authenticated:
        return redirect(url_for("auth_error"))
    return render_template("staff_info.html", title="Çalışan Bilgileri", staff_list=get_all_staff())


@APP.route("/cancelbook", methods=['GET', 'POST'])
def cancel_book():
    form = CustomerCancelForm()

    if form.validate_on_submit():
        tckn = form.tckn.data
        cust = Customer.query.filter_by(tckn=tckn).first()
        if cust and cust.bookings:
            cust.bookings[-1].is_cancelled = True
            db.session.commit()

        return render_template("book_cancel_info.html", title="İptal Talebi Başarılı")
    return render_template("book_cancel.html", title="Rezervasyon İptali", form=form)


@APP.route("/rezervasyon", methods=['GET', 'POST'])
@APP.route("/booking", methods=['GET', 'POST'])
def book_room():
    form = CustomerBookingForm()

    if form.validate_on_submit():
        e_room = get_min_empty_room_number()

        cust = Customer(tckn=form.tckn.data, fname=form.fname.data, sname=form.sname.data,
                        is_inside=False, phone=form.phone.data)
        book = Booking(room=e_room, checkin=form.startdate.data,
                       checkout=form.enddate.data, is_online=True, is_cancelled=False)

        if Customer.query.filter_by(tckn=cust.tckn).all():
            cust = Customer.query.filter_by(tckn=cust.tckn).first()
        else:
            # New customer
            cust.occ_count = 0
            cust.card_num = randint(10000, 999999)
            db.session.add(cust)

        # Mark room as full
        booked_room = Room.query.filter_by(id=e_room).first()
        # booked_room.is_full = True
        booked_room.reserv_date = form.startdate.data

        db.session.add(book)
        book.bookers.append(cust)
        db.session.commit()
        return redirect(url_for("book_thanks"))
    return render_template("book_room.html", title="Otel Rezervasyonu", form=form)


@APP.route("/thanks", methods=['GET', 'POST'])
def book_thanks():
    return render_template("book_thanks.html", title="Teşekkürler!")


@APP.route("/", methods=['GET', 'POST'])
@APP.route("/home", methods=['GET', 'POST'])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for("auth_error"))

    h_info = []  # Room info
    o_info = []  # Online booking info
    tmp = []
    for idx, cust_and_room in enumerate(get_customers_rooms()):
        tmp.append(cust_and_room)
        if (idx+1) % 3 == 0:
            h_info.append(tmp)
            tmp = []
    h_info.append(tmp)

    tmp = []
    for idx, cust_and_room in enumerate(get_reserved_customers()):
        tmp.append(cust_and_room)
        if (idx+1) % 3 == 0:
            o_info.append(tmp)
            tmp = []
    o_info.append(tmp)

    return render_template("home.html", hotel_info=h_info, o_info=o_info,
                           num_cust=number_of_customer_inside(),
                           num_online=number_of_online_books())


@APP.route("/about")
def about():
    return render_template("about.html", title="About")


@APP.route("/hotel_settings", methods=['GET', 'POST'])
def hotel_settings():
    if not current_user.is_authenticated:
        return redirect(url_for("auth_error"))

    room_form = AddRoomForm()
    if room_form.validate_on_submit():
        room_range = range(room_form.num_from.data, room_form.num_to.data + 1)
        for rm_num in room_range:
            new_room = Room(id=rm_num, capacity=room_form.capacity.data, is_full=False)
            db.session.add(new_room)

        db.session.commit()
        flash("{} - {} arası bütün odalar eklendi.".format(room_form.num_from.data,
                                                           room_form.num_to.data), "success")

    staff_form = AddStaffForm()
    if staff_form.validate_on_submit():
        staff = Staff(tckn=staff_form.tckn.data, fname=staff_form.fname.data,
                      sname=staff_form.sname.data, position=staff_form.position.data,
                      salary=int(staff_form.salary.data*10000))

        db.session.add(staff)
        db.session.commit()
        flash('Çalışan başarıyla eklendi', 'success')

    return render_template("hotel_settings.html", title="Otel Paneli", room_form=room_form,
                           staff_form=staff_form, staff_positons=["Müdür", "Sekreter"],
                           def_room_num=get_max_room_number()+1)


@APP.route("/customer_in", methods=['GET', 'POST'])
def customer_in():
    if not current_user.is_authenticated:
        flash("Yetkili kullanıcı olarak giriş yapınız.", "danger")
        return redirect(url_for("auth_error"))

    form = CustomerInForm()
    if form.validate_on_submit():
        cust = Customer(tckn=form.tckn.data, fname=form.fname.data, sname=form.sname.data,
                        is_inside=True, phone=form.phone.data)
        book = Booking(room=form.room.data, checkin=form.checkin.data, checkout=form.checkout.data,
                       is_online=False, is_cancelled=False)

        if Customer.query.filter_by(tckn=cust.tckn).all():
            flash(f"Müşterimizin ilk seferi değil.")
            cust = Customer.query.filter_by(tckn=cust.tckn).first()
            cust.is_inside = True
            cust.occ_count += 1
        else:
            # New customer
            cust.occ_count = 0
            cust.card_num = randint(10000, 999999)
            db.session.add(cust)

        # Mark room as full
        Room.query.filter_by(id=form.room.data).first().is_full = True

        db.session.add(book)
        book.bookers.append(cust)
        db.session.commit()
        flash('Müşteri girişi başarılı!', 'success')
        return redirect(url_for('customer_in'))

    return render_template("customer_in.html", title="Yeni Müşteri Girişi", form=form,
                           room_suggest=get_min_empty_room_number())


@APP.route("/customer_out", methods=['GET', 'POST'])
def customer_out():
    if not current_user.is_authenticated:
        flash("Yetkili kullanıcı olarak giriş yapınız.", "danger")
        return redirect(url_for("auth_error"))

    form = CustomerOutForm()
    if form.validate_on_submit():
        cust = Customer.query.filter_by(tckn=form.tckn.data).first()
        if cust:
            if cust.is_inside:
                cust.is_inside = False

                Room.query.filter_by(id=cust.bookings[-1].room).first().is_full = False
                db.session.commit()
                flash('Müşteri çıkışı başarılı!', 'success')
            else:
                flash(f'Müşteri daha önce çıkış yapmış.')
        else:
            flash(f'Müşteri bulunamadı.', 'danger')

    return render_template("customer_out.html", title="Müşteri Çıkışı", form=form)


@APP.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)\
                          .decode("utf-8")
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)


@APP.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Logging unsuccessful!', 'danger')
    return render_template("login.html", title="Login", form=form)


@APP.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@APP.route("/customerinfo", methods=["GET", "POST"])
def customer_info():
    return render_template("customer_info.html", title="Müşteri Bilgisi", cust_list=get_all_customers())


@APP.route("/autherror", methods=['GET', 'POST'])
def auth_error():
    return render_template("auth_error.html", title="Yetki Yok")
