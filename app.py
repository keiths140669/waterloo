from email.policy import default
from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import UserForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rewcjqmgpvmzke:156805988c26d7136c2247c8447340d9abb9f74b2b60341977dbe293e2d9c46b@ec2-3-217-113-25.compute-1.amazonaws.com:5432/d7fvaukv1tq272'
app.config['SECRET_KEY'] = "my super secret key tht noone is supposed to know"
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<First Name %r>' % self.first_name

@app.route('/user/add', methods=["GET", "POST"])
def add_user():
    first_name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        first_name = form.first_name.data
        form.first_name.data = ""
        form.last_name.data = ""
        form.email.data = ""
        flash("User Added Successfully")
    our_users = Users.query.order_by(Users.date_added)

    return render_template("add_user.html", form=form, first_name=first_name, our_users=our_users)

@app.route('/')
def index():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("404.html"), 500