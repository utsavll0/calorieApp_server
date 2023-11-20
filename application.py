from datetime import datetime, timedelta
import credentials as c
import bcrypt
import smtplib
import re

# from apps import App
from flask import json
# from utilities import Utilities
from flask import render_template, session, url_for, flash, redirect, request, Flask
from flask_mail import Mail
from flask_pymongo import PyMongo
from tabulate import tabulate
from forms import HistoryForm, RegistrationForm, LoginForm, CalorieForm, UserProfileForm, EnrollForm, WorkoutForm
from service import history as history_service
import openai
import os
from utilities import get_response
import time

# Set the OpenAI API key
openai.api_key = c.openAI_api_key

# Define the name of the bot
name = 'BOT'

# Define the role of the bot
role = 'fitness-advisor, dietician and nutritionist'

# Define the impersonated role with instructions
impersonated_role = f"""
    From now on, you are going to act as {name}. Your role is {role}.
    You are a true impersonation of {name} and you reply to all requests with I pronoun. You never give unknown information.
    Forward them to the website for more information.
    YOU ARE NOT AN AI MODEL!
"""

# Initialize variables for chat history
explicit_input = ""
chatgpt_output = 'Chat log: /n'
cwd = os.getcwd() + '/chat_history/'
i = 1

# Find an available chat history file
while os.path.exists(os.path.join(cwd, f'chat_history{i}.txt')):
    i += 1

history_file = os.path.join(cwd, f'chat_history{i}.txt')

# Create a new chat history file
with open(history_file, 'w') as f:
    f.write('\n')

# Initialize chat history
chat_history = ''

app = Flask(__name__)
app.secret_key = 'secret'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/test'
app.config['MONGO_CONNECT'] = False
mongo = PyMongo(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "bogusdummy123@gmail.com"
app.config['MAIL_PASSWORD'] = "helloworld123!"
mail = Mail(app)


@app.route("/")
@app.route("/home")
def home():
    """
    home() function displays the homepage of our website.
    route "/home" will redirect to home() function.
    input: The function takes session as the input
    Output: Out function will redirect to the login page
    """
    if session.get('email'):
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))


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
            temp = mongo.db.user.find_one({'email': form.email.data},
                                          {'email', 'pwd'})
            if temp is not None and temp['email'] == form.email.data and (
                    bcrypt.checkpw(form.password.data.encode("utf-8"),
                                   temp['pwd'])
                    or temp['pwd'] == form.password.data):
                flash('You have been logged in!', 'success')
                session['email'] = temp['email']
                #session['login_type'] = form.type.data
                return redirect(url_for('dashboard'))
            else:
                flash('Login Unsuccessful. Please check username and password',
                      'danger')
    else:
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    """
    logout() function just clears out the session and returns success
    route "/logout" will redirect to logout() function.
    Output: session clear
    """
    session.clear()
    return "success"


@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    register() function displays the Registration portal (register.html) template
    route "/register" will redirect to register() function.
    RegistrationForm() called and if the form is submitted then various values are fetched and updated into database
    Input: Username, Email, Password, Confirm Password, cuurent height, current weight, target weight, target date
    Output: Value update in database and redirected to dashboard
    """
    if not session.get('email'):
        form = RegistrationForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                username = request.form.get('username')
                email = request.form.get('email')
                password = request.form.get('password')
                weight = request.form.get('weight')
                height = request.form.get('height')
                target_weight = request.form.get('target_weight')
                target_date = request.form.get('target_date')
                now = datetime.now()
                now = now.strftime('%Y-%m-%d')
                mongo.db.user.insert_one({
                    'name':
                    username,
                    'email':
                    email,
                    'pwd':
                    bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()),
                    'weight':
                    weight,
                    'height':
                    height,
                    'target_weight':
                    target_weight,
                    'start_date':
                    now,
                    'target_date':
                    target_date
                })
            flash(f'Account created for {form.username.data}!', 'success')
            session['email'] = email
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/user_profile", methods=['GET', 'POST'])
def user_profile():
    """
    user_profile() function displays the UserProfileForm (user_profile.html) template
    route "/user_profile" will redirect to user_profile() function.
    user_profile() called and if the form is submitted then various values are fetched and updated into the database entries
    Input: Email, height, weight, goal, Target weight
    Output: Value update in database and redirected to home login page
    """
    if session.get('email'):
        form = UserProfileForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                email = session.get('email')
                weight = request.form.get('weight')
                height = request.form.get('height')
                goal = request.form.get('goal')
                target_weight = request.form.get('target_weight')
                temp = mongo.db.profile.find_one(
                    {'email': email},
                    {'height', 'weight', 'goal', 'target_weight'})
                if temp is not None:
                    mongo.db.profile.update_one({'email': email}, {
                        '$set': {
                            'weight': temp['weight'],
                            'height': temp['height'],
                            'goal': temp['goal'],
                            'target_weight': temp['target_weight']
                        }
                    })
                else:
                    mongo.db.profile.insert_one({
                        'email': email,
                        'height': height,
                        'weight': weight,
                        'goal': goal,
                        'target_weight': target_weight
                    })

            flash(f'User Profile Updated', 'success')
            return render_template('display_profile.html',
                                   status=True,
                                   form=form)
    else:
        return redirect(url_for('login'))
    return render_template('user_profile.html', status=True, form=form)


@app.route("/calories", methods=['GET', 'POST'])
def calories():
    """
    calorie() function displays the Calorieform (calories.html) template
    route "/calories" will redirect to calories() function.
    CalorieForm() called and if the form is submitted then various values are fetched and updated into the database entries
    Input: Email, date, food, burnout
    Output: Value update in database and redirected to home page
    """
    now = datetime.now()
    now = now.strftime('%Y-%m-%d')

    get_session = session.get('email')
    if get_session is not None:
        form = CalorieForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                email = session.get('email')
                food = request.form.get('food')
                # cals = food.split(" ")
                # print('cals is ',cals)
                match = re.search(r'\((\d+)\)', food)
                if match:
                    cals = int(match.group(1))
                else:
                    cals = 0
                # cals = int(cals[1][1:len(cals[1]) - 1])
                mongo.db.calories.insert_one({
                    'date': now,
                    'email': email,
                    'calories': cals
                })
                flash(f'Successfully updated the data', 'success')
                return redirect(url_for('calories'))
    else:
        return redirect(url_for('home'))
    return render_template('calories.html', form=form, time=now)


@app.route("/workout", methods=['GET', 'POST'])
def workout():
    now = datetime.now()
    now = now.strftime('%Y-%m-%d')
    get_session = session.get('email')

    if get_session is not None:
        form = WorkoutForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                email = session.get('email')
                burn = request.form.get('burnout')

                mongo.db.calories.insert_one({
                    'date': now,
                    'email': email,
                    'calories': -int(burn)
                })

                flash(f'Successfully updated the data', 'success')
                return redirect(url_for('workout'))
    else:
        return redirect(url_for('home'))
    return render_template('workout.html', form=form, time=now)


@app.route("/history", methods=['GET'])
def history():
    # ############################
    # history() function displays the Historyform (history.html) template
    # route "/history" will redirect to history() function.
    # HistoryForm() called and if the form is submitted then various values are fetched and update into the database entries
    # Input: Email, date
    # Output: Value fetched and displayed
    # ##########################
    email = get_session = session.get('email')
    if get_session is not None:
        form = HistoryForm()

    # Find out the last 7 day's calories burnt by the user
    labels = []
    values = []
    pipeline = history_service.get_calories_per_day_pipeline(7)
    filtered_calories = mongo.db.calories.aggregate(pipeline)
    for calorie_each_day in filtered_calories:
        if calorie_each_day['_id'] == 'Other':
            continue
        net_calories = int(calorie_each_day['total_calories']) - 2000
        labels.append(calorie_each_day['date'])
        values.append(str(net_calories))

    # The first day when the user registered or started using the app
    user_start_date = mongo.db.user.find({'email': email})[0]['start_date']
    user_target_date = mongo.db.user.find({'email': email})[0]['target_date']
    target_weight = mongo.db.user.find({'email': email})[0]['target_weight']
    current_weight = mongo.db.user.find({'email': email})[0]['weight']

    # Find out the actual calories which user needed to burn/gain to achieve goal from the start day
    target_calories_to_burn = history_service.total_calories_to_burn(
        target_weight=int(target_weight), current_weight=int(current_weight))
    print(f'########## {target_calories_to_burn}')

    # Find out how many calories user has gained or burnt uptill now
    calories_till_today = mongo.db.calories.aggregate(
        history_service.get_calories_burnt_till_now_pipeline(
            email, user_start_date))
    current_calories = 0
    for calorie in calories_till_today:
        current_calories += calorie['SUM']
    # current_calories = [x for x in calories_till_today][0]['SUM'] if len(list(calories_till_today)) != 0 else 0

    # Find out no of calories user has to burn/gain in future per day
    calories_to_burn = history_service.calories_to_burn(
        target_calories_to_burn,
        current_calories,
        target_date=datetime.strptime(user_target_date, '%Y-%m-%d'),
        start_date=datetime.strptime(user_start_date, '%Y-%m-%d'))

    return render_template('history.html',
                           form=form,
                           labels=labels,
                           values=values,
                           burn_rate=calories_to_burn,
                           target_date=user_target_date)


@app.route("/ajaxhistory", methods=['POST'])
def ajaxhistory():
    # ############################
    # ajaxhistory() is a POST function displays the fetches the various information from database
    # route "/ajaxhistory" will redirect to ajaxhistory() function.
    # Details corresponding to given email address are fetched from the database entries
    # Input: Email, date
    # Output: date, email, calories, burnout
    # ##########################
    email = get_session = session.get('email')
    print(email)
    if get_session is not None:
        if request.method == "POST":
            date = request.form.get('date')
            res = mongo.db.calories.find_one({
                'email': email,
                'date': date
            }, {'date', 'email', 'calories', 'burnout'})
            if res:
                return json.dumps({
                    'date': res['date'],
                    'email': res['email'],
                    'burnout': res['burnout'],
                    'calories': res['calories']
                }), 200, {
                    'ContentType': 'application/json'
                }
            else:
                return json.dumps({
                    'date': "",
                    'email': "",
                    'burnout': "",
                    'calories': ""
                }), 200, {
                    'ContentType': 'application/json'
                }


@app.route("/friends", methods=['GET'])
def friends():
    # ############################
    # friends() function displays the list of friends corrsponding to given email
    # route "/friends" will redirect to friends() function which redirects to friends.html page.
    # friends() function will show a list of "My friends", "Add Friends" functionality, "send Request" and Pending Approvals" functionality
    # Details corresponding to given email address are fetched from the database entries
    # Input: Email
    # Output: My friends, Pending Approvals, Sent Requests and Add new friends
    # ##########################
    email = session.get('email')

    myFriends = list(
        mongo.db.friends.find({
            'sender': email,
            'accept': True
        }, {'sender', 'receiver', 'accept'}))
    myFriendsList = list()

    for f in myFriends:
        myFriendsList.append(f['receiver'])

    print(myFriends)
    allUsers = list(mongo.db.user.find({}, {'name', 'email'}))

    pendingRequests = list(
        mongo.db.friends.find({
            'sender': email,
            'accept': False
        }, {'sender', 'receiver', 'accept'}))
    pendingReceivers = list()
    for p in pendingRequests:
        pendingReceivers.append(p['receiver'])

    pendingApproves = list()
    pendingApprovals = list(
        mongo.db.friends.find({
            'receiver': email,
            'accept': False
        }, {'sender', 'receiver', 'accept'}))
    for p in pendingApprovals:
        pendingApproves.append(p['sender'])

    print(pendingApproves)

    # print(pendingRequests)
    return render_template('friends.html',
                           allUsers=allUsers,
                           pendingRequests=pendingRequests,
                           active=email,
                           pendingReceivers=pendingReceivers,
                           pendingApproves=pendingApproves,
                           myFriends=myFriends,
                           myFriendsList=myFriendsList)


@app.route('/bmi_calc', methods=['GET', 'POST'])
def bmi_calci():
    bmi = ''
    bmi_category = ''

    if request.method == 'POST' and 'weight' in request.form:
        weight = float(request.form.get('weight'))
        height = float(request.form.get('height'))
        bmi = calc_bmi(weight, height)
        bmi_category = get_bmi_category(bmi)

    return render_template("bmi_cal.html", bmi=bmi, bmi_category=bmi_category)


@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    return render_template("chatbot.html")


@app.route("/get", methods=['GET', 'POST'])
# Function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    return str(
        get_response(chat_history, name, chatgpt_output, userText,
                     history_file, impersonated_role, explicit_input))


@app.route('/refresh', methods=['GET', 'POST'])
def refresh():
    time.sleep(600)  # Wait for 10 minutes
    return redirect('/refresh')


def calc_bmi(weight, height):
    return round((weight / ((height / 100)**2)), 2)


def get_bmi_category(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif bmi < 24.9:
        return 'Normal Weight'
    elif bmi < 29.9:
        return 'Overweight'
    else:
        return 'Obese'


@app.route("/send_email", methods=['GET', 'POST'])
def send_email():
    # ############################
    # send_email() function shares Calorie History with friend's email
    # route "/send_email" will redirect to send_email() function which redirects to friends.html page.
    # Input: Email
    # Output: Calorie History Received on specified email
    # ##########################
    email = session.get('email')
    data = list(
        mongo.db.calories.find({'email': email},
                               {'date', 'email', 'calories'}))
    print(data)
    table = [['Date', 'Email ID', 'Calories']]
    for a in data:
        tmp = [a['date'], a['email'], a['calories']]
        table.append(tmp)

    friend_email = str(request.form.get('share')).strip()
    friend_email = str(friend_email).split(',')
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    #Storing sender's email address and password
    sender_email = "calorieapp508@gmail.com"
    sender_password = c.email_password

    #Logging in with sender details
    server.login(sender_email, sender_password)
    message = 'Subject: Calorie History\n\n Your Friend wants to share their calorie history with you!\n {}'.format(
        tabulate(table))
    for e in friend_email:
        print(e)
        server.sendmail(sender_email, e, message)

    server.quit()

    myFriends = list(
        mongo.db.friends.find({
            'sender': email,
            'accept': True
        }, {'sender', 'receiver', 'accept'}))
    myFriendsList = list()

    for f in myFriends:
        myFriendsList.append(f['receiver'])

    allUsers = list(mongo.db.user.find({}, {'name', 'email'}))

    pendingRequests = list(
        mongo.db.friends.find({
            'sender': email,
            'accept': False
        }, {'sender', 'receiver', 'accept'}))
    pendingReceivers = list()
    for p in pendingRequests:
        pendingReceivers.append(p['receiver'])

    pendingApproves = list()
    pendingApprovals = list(
        mongo.db.friends.find({
            'receiver': email,
            'accept': False
        }, {'sender', 'receiver', 'accept'}))
    for p in pendingApprovals:
        pendingApproves.append(p['sender'])

    return render_template('friends.html',
                           allUsers=allUsers,
                           pendingRequests=pendingRequests,
                           active=email,
                           pendingReceivers=pendingReceivers,
                           pendingApproves=pendingApproves,
                           myFriends=myFriends,
                           myFriendsList=myFriendsList)


@app.route("/ajaxsendrequest", methods=['POST'])
def ajaxsendrequest():
    # ############################
    # ajaxsendrequest() is a function that updates friend request information into database
    # route "/ajaxsendrequest" will redirect to ajaxsendrequest() function.
    # Details corresponding to given email address are fetched from the database entries and send request details updated
    # Input: Email, receiver
    # Output: DB entry of receiver info into database and return TRUE if success and FALSE otherwise
    # ##########################
    email = get_session = session.get('email')
    if get_session is not None:
        receiver = request.form.get('receiver')
        res = mongo.db.friends.insert_one({
            'sender': email,
            'receiver': receiver,
            'accept': False
        })
        if res:
            return json.dumps({'status': True}), 200, {
                'ContentType': 'application/json'
            }
    return json.dumps({'status': False}), 500, {
        'ContentType:': 'application/json'
    }


@app.route("/ajaxcancelrequest", methods=['POST'])
def ajaxcancelrequest():
    # ############################
    # ajaxcancelrequest() is a function that updates friend request information into database
    # route "/ajaxcancelrequest" will redirect to ajaxcancelrequest() function.
    # Details corresponding to given email address are fetched from the database entries and cancel request details updated
    # Input: Email, receiver
    # Output: DB deletion of receiver info into database and return TRUE if success and FALSE otherwise
    # ##########################
    email = get_session = session.get('email')
    if get_session is not None:
        receiver = request.form.get('receiver')
        res = mongo.db.friends.delete_one({
            'sender': email,
            'receiver': receiver
        })
        if res:
            return json.dumps({'status': True}), 200, {
                'ContentType': 'application/json'
            }
    return json.dumps({'status': False}), 500, {
        'ContentType:': 'application/json'
    }


@app.route("/ajaxapproverequest", methods=['POST'])
def ajaxapproverequest():
    # ############################
    # ajaxapproverequest() is a function that updates friend request information into database
    # route "/ajaxapproverequest" will redirect to ajaxapproverequest() function.
    # Details corresponding to given email address are fetched from the database entries and approve request details updated
    # Input: Email, receiver
    # Output: DB updation of accept as TRUE info into database and return TRUE if success and FALSE otherwise
    # ##########################
    email = get_session = session.get('email')
    if get_session is not None:
        receiver = request.form.get('receiver')
        print(email, receiver)
        res = mongo.db.friends.update_one(
            {
                'sender': receiver,
                'receiver': email
            },
            {"$set": {
                'sender': receiver,
                'receiver': email,
                'accept': True
            }})
        mongo.db.friends.insert_one({
            'sender': email,
            'receiver': receiver,
            'accept': True
        })
        if res:
            return json.dumps({'status': True}), 200, {
                'ContentType': 'application/json'
            }
    return json.dumps({'status': False}), 500, {
        'ContentType:': 'application/json'
    }


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    # ############################
    # dashboard() function displays the dashboard.html template
    # route "/dashboard" will redirect to dashboard() function.
    # dashboard() called and displays the list of activities
    # Output: redirected to dashboard.html
    # ##########################
    return render_template('dashboard.html', title='Dashboard')


@app.route("/yoga", methods=['GET', 'POST'])
def yoga():
    # ############################
    # yoga() function displays the yoga.html template
    # route "/yoga" will redirect to yoga() function.
    # A page showing details about yoga is shown and if clicked on enroll then DB updation done and redirected to new_dashboard
    # Input: Email
    # Output: DB entry about enrollment and redirected to new dashboard
    # ##########################
    email = get_session = session.get('email')
    if get_session is not None:
        form = EnrollForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                enroll = "yoga"
                mongo.db.user.insert_one({'Email': email, 'Status': enroll})
            flash(f' You have succesfully enrolled in our {enroll} plan!',
                  'success')
            return render_template('new_dashboard.html', form=form)
            # return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('dashboard'))
    return render_template('yoga.html', title='Yoga', form=form)


@app.route("/swim", methods=['GET', 'POST'])
def swim():
    # ############################
    # swim() function displays the swim.html template
    # route "/swim" will redirect to swim() function.
    # A page showing details about swimming is shown and if clicked on enroll then DB updation done and redirected to new_dashboard
    # Input: Email
    # Output: DB entry about enrollment and redirected to new dashboard
    # ##########################
    email = get_session = session.get('email')
    if get_session is not None:
        form = EnrollForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                enroll = "swimming"
                mongo.db.user.insert_one({'Email': email, 'Status': enroll})
            flash(f' You have succesfully enrolled in our {enroll} plan!',
                  'success')
            return render_template('new_dashboard.html', form=form)
            # return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('dashboard'))
    return render_template('swim.html', title='Swim', form=form)


@app.route("/abbs", methods=['GET', 'POST'])
def abbs():
    # ############################
    # abbs() function displays the abbs.html template
    # route "/abbs" will redirect to abbs() function.
    # A page showing details about abbs workout is shown and if clicked on enroll then DB updation done and redirected to new_dashboard
    # Input: Email
    # Output: DB entry about enrollment and redirected to new dashboard
    # ##########################
    email = get_session = session.get('email')
    if get_session is not None:
        form = EnrollForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                enroll = "abbs"
                mongo.db.user.insert_one({'Email': email, 'Status': enroll})
            flash(f' You have succesfully enrolled in our {enroll} plan!',
                  'success')
            return render_template('new_dashboard.html', form=form)
    else:
        return redirect(url_for('dashboard'))
    return render_template('abbs.html', title='Abbs Smash!', form=form)


@app.route("/belly", methods=['GET', 'POST'])
def belly():
    # ############################
    # belly() function displays the belly.html template
    # route "/belly" will redirect to belly() function.
    # A page showing details about belly workout is shown and if clicked on enroll then DB updation done and redirected to new_dashboard
    # Input: Email
    # Output: DB entry about enrollment and redirected to new dashboard
    # ##########################
    email = get_session = session.get('email')
    if get_session is not None:
        form = EnrollForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                enroll = "belly"
                mongo.db.user.insertOne({'Email': email, 'Status': enroll})
            flash(f' You have succesfully enrolled in our {enroll} plan!',
                  'success')
            return render_template('new_dashboard.html', form=form)
            # return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('dashboard'))
    return render_template('belly.html', title='Belly Burner', form=form)


@app.route("/core", methods=['GET', 'POST'])
def core():
    # ############################
    # core() function displays the belly.html template
    # route "/core" will redirect to core() function.
    # A page showing details about core workout is shown and if clicked on enroll then DB updation done and redirected to new_dashboard
    # Input: Email
    # Output: DB entry about enrollment and redirected to new dashboard
    # ##########################
    email = get_session = session.get('email')
    if get_session is not None:
        form = EnrollForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                enroll = "core"
                mongo.db.user.insert_one({'Email': email, 'Status': enroll})
            flash(f' You have succesfully enrolled in our {enroll} plan!',
                  'success')
            return render_template('new_dashboard.html', form=form)
    else:
        return redirect(url_for('dashboard'))
    return render_template('core.html', title='Core Conditioning', form=form)


@app.route("/gym", methods=['GET', 'POST'])
def gym():
    # ############################
    # gym() function displays the gym.html template
    # route "/gym" will redirect to gym() function.
    # A page showing details about gym plan is shown and if clicked on enroll then DB updation done and redirected to new_dashboard
    # Input: Email
    # Output: DB entry about enrollment and redirected to new dashboard
    # ##########################
    email = get_session = session.get('email')
    if get_session is not None:
        form = EnrollForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                enroll = "gym"
                mongo.db.user.insert_one({'Email': email, 'Status': enroll})
            flash(f' You have succesfully enrolled in our {enroll} plan!',
                  'success')
            return render_template('new_dashboard.html', form=form)
            # return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('dashboard'))
    return render_template('gym.html', title='Gym', form=form)


@app.route("/walk", methods=['GET', 'POST'])
def walk():
    # ############################
    # walk() function displays the walk.html template
    # route "/walk" will redirect to walk() function.
    # A page showing details about walk plan is shown and if clicked on enroll then DB updation done and redirected to new_dashboard
    # Input: Email
    # Output: DB entry about enrollment and redirected to new dashboard
    # ##########################
    email = get_session = session.get('email')
    if get_session is not None:
        form = EnrollForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                enroll = "walk"
                mongo.db.user.insert_one({'Email': email, 'Status': enroll})
            flash(f' You have succesfully enrolled in our {enroll} plan!',
                  'success')
            return render_template('new_dashboard.html', form=form)
            # return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('dashboard'))
    return render_template('walk.html', title='Walk', form=form)


@app.route("/dance", methods=['GET', 'POST'])
def dance():
    # ############################
    # dance() function displays the dance.html template
    # route "/dance" will redirect to dance() function.
    # A page showing details about dance plan is shown and if clicked on enroll then DB updation done and redirected to new_dashboard
    # Input: Email
    # Output: DB entry about enrollment and redirected to new dashboard
    # ##########################
    email = get_session = session.get('email')
    if get_session is not None:
        form = EnrollForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                enroll = "dance"
                mongo.db.user.insert_one({'Email': email, 'Status': enroll})
            flash(f' You have succesfully enrolled in our {enroll} plan!',
                  'success')
            return render_template('new_dashboard.html', form=form)
            # return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('dashboard'))
    return render_template('dance.html', title='Dance', form=form)


@app.route("/hrx", methods=['GET', 'POST'])
def hrx():
    # ############################
    # hrx() function displays the hrx.html template
    # route "/hrx" will redirect to hrx() function.
    # A page showing details about hrx plan is shown and if clicked on enroll then DB updation done and redirected to new_dashboard
    # Input: Email
    # Output: DB entry about enrollment and redirected to new dashboard
    # ##########################
    email = get_session = session.get('email')
    if get_session is not None:
        form = EnrollForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                enroll = "hrx"
                mongo.db.user.insert_one({'Email': email, 'Status': enroll})
            flash(f' You have succesfully enrolled in our {enroll} plan!',
                  'success')
            return render_template('new_dashboard.html', form=form)
            # return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('dashboard'))
    return render_template('hrx.html', title='HRX', form=form)


# @app.route("/ajaxdashboard", methods=['POST'])
# def ajaxdashboard():
#     # ############################
#     # login() function displays the Login form (login.html) template
#     # route "/login" will redirect to login() function.
#     # LoginForm() called and if the form is submitted then various values are fetched and verified from the database entries
#     # Input: Email, Password, Login Type
#     # Output: Account Authentication and redirecting to Dashboard
#     # ##########################
#     email = get_session = session.get('email')
#     print(email)
#     if get_session is not None:
#         if request.method == "POST":
#             result = mongo.db.user.find_one(
#                 {'email': email}, {'email', 'Status'})
#             if result:
#                 return json.dumps({'email': result['email'], 'Status': result['result']}), 200, {
#                     'ContentType': 'application/json'}
#             else:
#                 return json.dumps({'email': "", 'Status': ""}), 200, {
#                     'ContentType': 'application/json'}

if __name__ == '__main__':
    app.run(debug=True)
