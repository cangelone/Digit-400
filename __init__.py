import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from flask import Flask, render_template, url_for, flash,redirect, request,session
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from pymysql import escape_string as thwart
import gc
from db_connect import connection 
app = Flask(__name__)

APP_CONTENT = {
    "Home":[["Welcome","/Welcome/","Welcome to my app"],
            ["Background","/Background/","We had alot of fun making this app. Learn more about our story"],],
                        
    "Profile":[["User Profile","/profile/","This is where you can view any regular information"],
               ["Settings","/settings/","This will tell you where everything is"],
               ["Terms of service","/tos/","If you have any questions..."],],
    
    "Contact":[["Contact","/contact/","In order to contact me..."],],
}

app = Flask(__name__)

def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            falsh("Please Login!")
            return redirect(url_for('login'))
    return wrap
    
    
@app.route("/", methods=["GET","POST"])
def hello():
    return render_template("main.html")
    """
    try:
        c, conn = connection()
        if request.mehtod == "POST":
            entered_username = request.form['username']
            entered_password = request.form['passowrd']
            
            data = c.execute("SELECT * FROM users WHERE username = ('{0}')".format(thwart(request.form['username'])))
            
            data = c.fetchone()[2]
            
            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']
                flash("You are now logged in "+ session['username']+"!")
                
            
                return rediredt(url_for("dashboard"))
            else:
                error = "Invlaid Credentilas. Please try again."
                return render_template("login,html", error = error)
        else:
            return render_template("main.html")
            
    except Exception as e:
        return render_template("500.hmtl", error =  e)
"""
@app.route("/login/", methods=["GET","POST"])
def login():
    error = ""
    try:
        c, conn = connection()
        if request.mehtod == "POST":
            entered_username = request.form['username']
            entered_password = request.form['passowrd']
            
            flash(entered_username)
            flash(entered_password)
            
            data = c.execute("SELECT * FROM users WHERE username = ('{0}')".format(thwart(request.form['username'])))
            
            data = c.fetchone()[2]
            
            
            
            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']
                flash("You are now logged in "+ session['username']+"!")
                return redirect(url_for("dashboard"))
            
                
            else:
                error ="Invlaid Credentilas. Please try again."
                return render_template("login.html", error = error)
            
        else:
            return render_template("login.html")
            
            
    except:
        return render_template("login.hmtl", error =  error)
    
    
@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('main'))

    
class RegistrationForm(Form):
    username = TextField("Username", [validators.Length(min=4, max=20)])
    email = TextField("Email Address", [validators.Length(min=6, max=50)])
    password = PasswordField("New Password", [validators.Required(), validators.EqualTo("confirm", message="Password must match")])
    confirm = PasswordField("Repeat Password")
    accept_tos = BooleanField("I accept the Terms of Service and Privacy Notice", [validators.Required()])
    
@app.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)
        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))

            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username= ('{0}')".format((thwart(username))))
                    
            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template("register.html", form = form)
            else:
                c.execute("INSERT INTO users(username, password, email, tracking) VALUES ('{0}','{1}','{2}','{3}')".format(thwart(username),thwart(password),thwart(email),thwart("/dashboard/")))
            conn.commit()
            flash("Thanks for registering!")
            c.close()
            conn.close()
            gc.collect()

            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for("dashboard"))

        return render_template("register.html", form = form)
    except Exception as e:
        return(str(e))
                    
                    
    
@app.route("/dashboard/")
def dashboard():
    try:
        return render_template("dashboard.html", APP_CONTENT = APP_CONTENT)
    except Exception as e:
        return render_template("500.html", error = e)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html")

if __name__ == "__main__":
    app.run()
    
    
    
