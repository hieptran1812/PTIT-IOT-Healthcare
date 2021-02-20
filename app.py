from flask import Flask, render_template, request, redirect, url_for
import database #database from mongodb
from user.models import User
import bcrypt

app = Flask(__name__)
app.secret_key = "ptit"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')

@app.route('/doctor', methods=['GET'])
def doctor():
    return render_template('doctor.html')

@app.route('/patient', methods=['GET'])
def patient():
    return render_template('patient.html')

@app.route('/user_profile', methods=['GET'])
def user_profile():
    return render_template('user_profile.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/nhiptho', methods=['GET'])
def nhiptho():
    return render_template('nhiptho.html')

@app.route('/tiengho', methods=['GET'])
def tiengho():
    return render_template('tiengho.html')

@app.route('/tiengwheeze', methods=['GET'])
def tiengwheeze():
    return render_template('tiengwheeze.html')

@app.route('/tiengrale', methods=['GET'])
def tiengrale():
    return render_template('tiengrale.html')

@app.route('/tienggay', methods=['GET'])
def tienggay():
    return render_template('tienggay.html')

@app.route('/nhiptho/hieptran1812', methods=['GET'])
def test():
    return render_template('hieptran1812.html')

@app.route("/", methods=['POST'])
def login():
    return User().login()

@app.route("/signout")
def signout():
    return User().signout()

if __name__ == '__main__':
    app.run(port=8000)