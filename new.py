from flask import Flask, render_template,request,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,UserMixin
#from forms import LoginForm, RegisterForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField, IntegerField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)
login_manager= LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fname = db.Column(db.String(120),  nullable=False)
    lname = db.Column(db.String(120),  nullable=False)
    password = db.Column(db.String(120),  nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username

class LoginForm(Form):
    username = StringField("Username", validators=[validators.Length(min=3, max=25),
     validators.DataRequired(message="Please Fill This Field")])
    password = StringField("Password", validators=[validators.Length(min=3, max=25),
     validators.DataRequired(message="Please Fill This Field")])

class RegisterForm(Form):
    email = StringField("Email", 
    validators=[validators.Email(message="Please enter a valid email address")])
    password = StringField("Password", validators=[validators.Length(min=3, max=25), 
    validators.DataRequired(message="Please Fill This Field")])
    fname = StringField("First Name", validators=[validators.Length(min=3, max=25), 
    validators.DataRequired(message="Please Fill This Field")])
    lname = StringField("Last Name", validators=[validators.Length(min=3, max=25), 
    validators.DataRequired(message="Please Fill This Field")])
    username = StringField("Username", validators=[validators.Length(min=3, max=25), 
    validators.DataRequired(message="Please Fill This Field")])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/main')
def main():
    return render_template("main.html")

@app.route('/register', methods=["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if request.method== "POST" and form.validate():
        try:
            user = User(
            username = form.username.data,
            email = form.email.data,
            fname = form.fname.data,
            lname = form.lname.data,
            password = form.password.data
            )
            db.session.add(user)
            db.session.commit() 
            flash("Yipee! you've registered successfully...!","success")
            return redirect("/login")
        except Exception as e:
            print("Failed to register.")
            print(e)
    return render_template("register.html", form = form)


@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm(request.form)
    if request.method== "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username = form.username.data).first()
        if user and password == user.password: 
            login_user(user)
            return redirect('/')
        else:
            flash('Invalid Credentials',warning)
            return redirect('/login')
        
    return render_template("login.html", form = form)
    


if __name__ == '__main__':
    app.run(debug=True)
