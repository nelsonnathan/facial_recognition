from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Separator


# initialization section
app = Flask(__name__)
bootstrap = Bootstrap(app)
nav = Nav(app)


# navigation section
def my_navbar():
    navbar = Navbar(title='recognition')
    navbar.items = [View('Home', 'home')]

    return navbar

nav.register_element('my_navbar', my_navbar)



# routes section
@app.route('/')
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)