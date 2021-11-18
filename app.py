from re import I
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Separator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, MacAddress
import keys as keys
from models import db, Users, Uploads
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash


# initialization section
app = Flask(__name__)
bootstrap = Bootstrap(app)
nav = Nav(app)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{keys.PSql}@localhost/recognition'
else:
    app.debug = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(db, app)


# database classes
class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=80)])

with app.app_context():
    db.create_all()


# navigation section
def unauth_navbar():
    navbar = Navbar(title='recognition')
    navbar.items = [View('Home', 'home'), View(
        'Login', 'login'), View('Sign Up', 'signup')]

    return navbar


nav.register_element('my_navbar', unauth_navbar)


# routes section
@app.route('/')
def home():
    return render_template("home.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_pass = generate_password_hash(
            form.password.data, method='sha256'
        )
        new_user = Users(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>User creation success!</h1>'
    
    return render_template('registration.html', form=form)


if __name__ == "__main__":
    app.run()
