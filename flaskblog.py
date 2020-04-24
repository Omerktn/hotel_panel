from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import secrets

APP = Flask(__name__)
APP.config['SECRET_KEY'] = secrets.token_hex(8) + "cx1m6%_3"
APP.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(APP)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


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


@APP.route("/", methods=['GET', 'POST'])
@APP.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("home.html", posts=posts)


@APP.route("/about")
def about():
    return render_template("about.html", title="About")


@APP.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Acoount crated for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template("register.html", title="Register", form=form)


@APP.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@sctr.com" and \
           form.password.data == "kürt_ali":
            flash(f'Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Logging unsuccessfull!', 'danger')
    return render_template("login.html", title="Login", form=form)


if __name__ == '__main__':
    APP.run(debug=True)
