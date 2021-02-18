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
    users = database.db.users
    login_user = users.find_one({'username': request.form['username']})

    if login_user:
        if brcypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('/'))
    return 'Invalid username or password combination'

if __name__ == '__main__':
    app.run(port=8000)