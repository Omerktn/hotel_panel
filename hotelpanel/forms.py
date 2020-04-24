from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, \
    DateField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo,\
    ValidationError
from hotelpanel.models import User, Room, Staff
from hotelpanel.methods import get_staff_as_select
from flask_login import current_user
import datetime


class AddRoomForm(FlaskForm):
    capacity = IntegerField("Tekil kapasite", validators=[DataRequired()], default=1)
    num_from = IntegerField("Başlangıç Oda No", validators=[DataRequired()])
    num_to = IntegerField("Bitiş Oda No", validators=[DataRequired()])
    submit = SubmitField('Odaları Ekle')


class AddStaffForm(FlaskForm):
    fname = StringField('Ad', validators=[DataRequired()])
    sname = StringField('Soyad')
    tckn = IntegerField('T.C. Kimlik Numarası')
    position = SelectField("Pozisyon", choices=[("manager", "Yönetici"),
                                                ("service", "Servis Elemanı"),
                                                ("valet", "Vale"),
                                                ("kitchen", "Mutfak Görevlisi"),
                                                ("servant", "Temizlik Görevlisi"),
                                                ("recep", "Resepsiyonist"),
                                                ("spa", "Spa Görevlisi"),
                                                ("other", "Diğer")])
    supervisor = SelectField("Üst Yönetici", choices=get_staff_as_select())
    # StringField('Pozisyon', validators=[DataRequired()])
    salary = FloatField('Maaş')
    submit = SubmitField("Çalışan Ekle")

    def validate_tckn(self, tckn):
        tckn = Staff.query.filter_by(id=tckn.data).first()
        if tckn:
            raise ValidationError('Bu çalışan zaten bulunmakta.')


class CustomerBookingForm(FlaskForm):
    tckn = IntegerField('T.C. Kimlik Numarası', validators=[DataRequired()])
    fname = StringField('Ad', validators=[DataRequired()])
    sname = StringField('Soyad')
    startdate = DateField('Başlangıç Tarihi', default=datetime.date.today, format='%d-%m-%Y',
                          validators=[DataRequired()])
    enddate = DateField('Bitiş Tarihi', default=datetime.date.today,
                        format='%d-%m-%Y', validators=[DataRequired()])
    num_of_people = SelectField("Kişi Sayısı", choices=[("1", "1"),
                                                        ("2", "2"),
                                                        ("3", "3")])
    submit = SubmitField("Rezervasyon yap")

    def validate_tckn(self, tckn):
        if len(str(tckn)) != 11:
            pass
            # raise ValidationError("Geçerli bir T.C. No giriniz.")


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[
        DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('This email already exists.')


class LoginForm(FlaskForm):
    username = StringField('User', validators=[
        DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class CustomerInForm(FlaskForm):
    tckn = IntegerField("T.C. Kimlik Numarası", validators=[DataRequired()])
    fname = StringField("Ad", validators=[DataRequired()])
    sname = StringField("Soyad", validators=[DataRequired()])
    phone = StringField("Telefon Numarası", default="+90")
    room = IntegerField("Oda Numarası", validators=[DataRequired()])

    checkin = DateField("Giriş Tarihi", default=datetime.date.today, format='%d-%m-%Y',
                        validators=[DataRequired()])
    checkout = DateField("Çıkış Tarihi", default=datetime.date.today, format='%d-%m-%Y',
                         validators=[DataRequired()])
    submit = SubmitField("Yeni Kayıt")

    def validate_room(self, room):
        rm = Room.query.filter_by(id=room.data).first()
        if not rm:
            raise ValidationError("Oda mevcut değil".format(int(room.data)))
        elif rm and rm.is_full:
            raise ValidationError("Oda {} dolu.".format(int(room.data)))


class CustomerOutForm(FlaskForm):
    tckn = IntegerField("T.C. Kimlik Numarası", validators=[DataRequired()])
    outdate = DateField("Çıkış Tarihi", default=datetime.date.today, format='%d-%m-%Y',
                        validators=[DataRequired()])
    submit = SubmitField("Çıkışı Gerçekleştir")


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[
        DataRequired(), Email()])
    picture = FileField("Update Profile Picture", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data is not current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is taken.')

    def validate_email(self, email):
        if email.data is not current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('This email already exists.')
