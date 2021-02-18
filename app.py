from flask import Flask, render_template
import database #database from mongodb
import bcrypt

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')

@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    return render_template('user_profile.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route("/", methods=['POST'])
def login():
    users = database.db.users
    login_user = users.find_one({'username': request.form['username']})

    if login_user:
        if brcypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('/'))
    return 'Invalid username or password combination'

if __name__ == '__main__':
    app.run(port=8000)