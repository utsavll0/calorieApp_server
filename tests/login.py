from forms import LoginForm
from tests.application import app, mongo


import bcrypt
from flask import flash, redirect, render_template, session, url_for


@app.route("/login", methods=['GET', 'POST'])
def login():
    """"
    login() function displays the Login form (login.html) template
    route "/login" will redirect to login() function.
    LoginForm() called and if the form is submitted then various values are fetched and verified from the database entries
    Input: Email, Password, Login Type
    Output: Account Authentication and redirecting to Dashboard
    """
    if not session.get('email'):
        form = LoginForm()
        if form.validate_on_submit():
            temp = mongo.db.user.find_one({'email': form.email.data},{
                'email', 'pwd','temp'})
            # print('temp is ',temp['pwd'])
            if temp is not None and temp['email'] == form.email.data and (
                bcrypt.checkpw(
                    form.password.data.encode("utf-8"),
                    ('temp' in temp and temp['temp'] == form.password.data) or temp['pwd'] ) ) :
                    # print(temp['pwd'])
                flash('You have been logged in!', 'success')
                session['email'] = temp['email']
                #session['login_type'] = form.type.data
                return redirect(url_for('dashboard'))
            else:
                flash(
                    'Login Unsuccessful. Please check username and password',
                    'danger')
    else:
        return redirect(url_for('home'))
    return render_template(
        'login.html',
        title='Login',
        form=form)