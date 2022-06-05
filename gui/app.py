from flask import Flask, session, request, render_template
import forms

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def login():
    if not session.get('logged_in'):
        #If not logged in
        form = forms.LoginForm(request.form)

        # if request.method == 'POST':
        #     # If pressed login
        #     username = request.form['username'].lower()
        #     password = request.form['password']
        #     if form.validate():
        #         if helpers.credentials_valid(username, password):
        #             session['logged_in'] = True
        #             session['username'] = username
        #             return json.dumps({'status': 'Login successful'})
        #         return json.dumps({'status': 'Invalid user/pass'})
        #     #Form is not valid
        #     return json.dumps({'status': 'Both fields required'})
        return render_template('login.html', form=form)
    # user = helpers.get_user()
    # return render_template('home.html', user=user)


app.run(debug=True)