from flask import Flask, render_template, request, redirect, url_for
from user.models import User, db
import bcrypt

app = Flask(__name__)
app.secret_key = "ptit"
users = db.users.find({})

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return User().login()
    else:
        return render_template('index.html')

@app.route('/admin', methods=['GET'])
def admin():
    users = db.users.find({})
    return render_template('dashboard.html', users = users)

@app.route('/adduser', methods=['POST', 'GET'])
def adduser():
    if request.method == 'GET':
        return render_template('adduser.html')
    else: 
        return User().addUser()

@app.route('/doctor', methods=['GET'])
def doctor():
    patients = db.users.find({
        'role': 'patient'
    })
    return render_template('doctor.html', patients = patients)

@app.route('/patient', methods=['GET'])
def patient():
    return render_template('patient.html')

@app.route('/user_profile', methods=['GET'])
def user_profile():
    return render_template('user_profile.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else: 
        return User().register()

@app.route('/nhiptho', methods=['GET'])
def nhiptho():
    users = db.users.find({})
    return render_template('nhiptho.html', users = users)

@app.route('/tiengho', methods=['GET'])
def tiengho():
    users = db.users.find({})
    return render_template('tiengho.html', users = users)

@app.route('/tiengwheeze', methods=['GET'])
def tiengwheeze():
    users = db.users.find({})
    return render_template('tiengwheeze.html', users = users)

@app.route('/tiengrale', methods=['GET'])
def tiengrale():
    users = db.users.find({})
    return render_template('tiengrale.html', users = users)

@app.route('/tienggay', methods=['GET'])
def tienggay():
    users = db.users.find({})
    return render_template('tienggay.html', users = users)

@app.route('/nhiptho/hiep', methods=['GET'])
def test():
    return render_template('hieptran1812.html')

@app.route("/signout")
def signout():
    return User().signout()

if __name__ == '__main__':
    app.run(port=8000)