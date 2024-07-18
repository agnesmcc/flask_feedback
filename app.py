from flask import Flask, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def homepage():
    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()
        session['username'] = user.username
        return redirect(f'/users/{user.username}')
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Invalid username/password."]

    return render_template("login.html", form=form)

@app.route("/users/<username>")
def show_user(username):
    if "username" not in session or username != session["username"]:
        return redirect("/")
    user = User.query.filter_by(username=username).first()
    return render_template("user.html", user=user)

@app.route("/logout")
def logout():
    session.pop("username")
    return redirect("/")

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    if "username" not in session or username != session["username"]:
        return redirect("/")
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    return redirect("/")

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    if "username" not in session or username != session["username"]:
        return redirect("/")
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f"/users/{username}")
    return render_template("feedback.html", form=form)  
