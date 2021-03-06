from flask import Flask, render_template, request, redirect, url_for, session
from user.models import User, db
import bcrypt

app = Flask(__name__)
app.secret_key = "ptit"

# limit_for_authentication = [
#   'admin',
#   'adduser',
#   'doctor',
#   'patient',
#   'user_profile',
#   'giamsat',
# ]

not_need_authentication = [
    'index',
    'static'
]

@app.before_request
def before_request():
  session.permanent = True
# app.permanent_session_lifetime = timedelta(minutes=10)
  print(request.endpoint)
  if 'logged_in' not in session and request.endpoint not in not_need_authentication:
    return redirect("/")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return User().login()
    else:
        return render_template('index.html')

@app.route('/adduser', methods=['POST', 'GET'])
def adduser():
    if request.method == 'GET':
        return render_template('adduser.html')
    else: 
        return User().addUser()

# @app.route('/doctor', methods=['GET'])
# def doctor():
#     patients = db.users.find({
#         'role': 'Bệnh nhân'
#     })
#     return render_template('doctor.html', patients = patients)

# @app.route('/patient', methods=['GET'])
# def patient():
#     username = session['username']
#     user = db.users.find_one({
#         'username': username
#     })
#     return render_template('patient.html', user = user)

# @app.route('/admin', methods=['GET'])
# def admin():
#     users = db.users.find({})
#     return render_template('dashboard.html', users = users)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    username = session['username']
    userInfo = db.users.find_one({
        'username': username
    })
    if userInfo['role'] == 'Admin':
        users = db.users.find({})
        return render_template('dashboard.html', users = users)
    elif userInfo['role'] == 'Bác sĩ':
        patients = db.users.find({
            'role': 'Bệnh nhân'
        })
        return render_template('doctor.html', patients = patients)
    else:
        user = db.users.find_one({
            'username': username
        })
        return render_template('patient.html', user = user)

@app.route('/user_profile/<username>', methods=['GET', 'POST']) # xem profile bệnh nhân và update user profile
def user_profile(username):
    user = db.users.find_one({
        'username': username
    })
    name = session['username']
    if request.method == 'GET':
        return render_template('user_profile.html', user=user, name=name)
    if request.method == 'POST':
        return User().updateUser(username)

@app.route('/<tenloaigiamsat>/<username>', methods=['GET']) #link xem url của bệnh nhân
def urlPartient(tenloaigiamsat, username):
    user_url = db.users.find_one({
        'username': username
    })
    url = None
    if str(tenloaigiamsat) == 'nhiptho':
        url = str(user_url['urlnhiptho'])
    if str(tenloaigiamsat) == 'tiengho':
        url = str(user_url['urltiengho'])
    if str(tenloaigiamsat) == 'tiengwheeze':
        url = str(user_url['urltiengwheeze'])
    if str(tenloaigiamsat) == 'tiengrale':
        url = str(user_url['urltiengrale'])
    if str(tenloaigiamsat) == 'tienggay':
        url = str(user_url['urltienggay'])
    users_patient = db.users.find({
        'role': 'Bệnh nhân'
    })
    loaigiamsat = {
        'nhiptho': 'Nhịp thở',
        'tiengho': 'Tiếng ho',
        'tiengwheeze': 'Tiếng wheeze',
        'tiengrale': 'Tiếng rale',
        'tienggay': 'Tiếng gáy',
    }
    tengiamsat = None
    if tenloaigiamsat in loaigiamsat:
        tengiamsat = tenloaigiamsat
    return render_template('urlbenhnhan.html', tenloaigiamsat = tenloaigiamsat, username = username, giamsat = loaigiamsat, users = users_patient, url = url)

@app.route('/delete/<username>', methods=['GET'])
def delete_user(username):
    return User().deleteUser(username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else: 
        return User().register()

@app.route('/giamsat/<tenloaigiamsat>', methods=['GET'])
def giamsat(tenloaigiamsat):
    users = db.users.find({
        'role': 'Bệnh nhân'
    })
    loaigiamsat = {
        'nhiptho': 'Nhịp thở',
        'tiengho': 'Tiếng ho',
        'tiengwheeze': 'Tiếng wheeze',
        'tiengrale': 'Tiếng rale',
        'tienggay': 'Tiếng gáy',
    }
    tengiamsat = None
    if tenloaigiamsat in loaigiamsat:
        tengiamsat = tenloaigiamsat
        return render_template('giamsat.html', giamsat = loaigiamsat, users = users, tenloaigiamsat = tenloaigiamsat)

@app.route("/signout")
def signout():
    return User().signout()

if __name__ == '__main__':
    app.run(port=8008)