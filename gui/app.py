from flask import Flask, redirect, session, request, render_template, url_for
from gui.lib import UserSystem
import os
import json
from gui.database import LogReader

app = Flask(__name__)
usersystem = UserSystem('mongodb://db:27017')
logreader = LogReader('mongodb://db:27017')
app.secret_key = os.urandom(12)

def protected_resource(f):
    def decorated(*args, **kwargs):
        if session.get('user'):
            return f(*args, **kwargs)
        return redirect(url_for('login'))
    decorated.__name__ = f.__name__
    return decorated


@app.route("/", methods=['GET', 'POST'])
def login():
    if session.get('user'):
        return redirect(url_for('home'))
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = usersystem.login(username, password)
            session['user'] = user.to_json()
            return redirect(url_for('home'))
        else:
            return render_template('login.html')


@app.route("/main", methods=['GET'])
@protected_resource
def home():
    """Home page"""
    return render_template('home.html', user=session['user'])

@app.route("/logout", methods=["POST"])
@protected_resource
def logout():
    del session['user']
    return redirect(url_for('login'))


@app.route("/main/config")
@protected_resource
def configuration():
    """Configuration viewing and editing page."""
    pass

@app.route("/main/packets")
@protected_resource
def packets():
    """Viewing, exporting and deleting of packets in the database."""
    return render_template('packets.html', 
    lst=[x for x in logreader.simple_query()])


@app.route("/main/users")
@protected_resource
def usermanager():
    """Viewing and managing users."""
    pass


@app.route("/main/users/register", methods=['GET', 'POST'])
@protected_resource
def register():
    """Registering new users."""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_pass = request.form['confirmPassword']
        if password == confirm_pass:
            try:
                user = usersystem.register(username, email, password, {})
                msg = f'user["username"] registered successfully.'
            except Exception as e:
                msg = str(e)
        else:
            msg = 'Register failed: passwords do not match.'
        return render_template('register.html', msg=msg)
    else:
        #'GET'
        return render_template('register.html')


@app.route("/main/users/log")
@protected_resource
def logviewer():
    """Viewing and clearing the log."""
    pass

@app.route("/main/shutdown")
def shutdown_test():
    """Viewing and clearing the log."""
    global ev_exit
    ev_exit.set()



def main(ev):
    global ev_exit

    ev_exit = ev

    app.run(debug=True, host='0.0.0.0')

if __name__ == '__main__':
    main()