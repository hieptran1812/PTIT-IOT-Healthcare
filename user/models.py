from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from passlib.hash import pbkdf2_sha256
from flask_pymongo import pymongo

username = "customer_db"
password = "hiep1812"
database_name = "ptit-wav2vec"

CONNECTION_STRING = "mongodb+srv://" + username + ":" + password + "@cluster0.dv4jr.mongodb.net/" + database_name + "?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database(database_name)

class User:
    
    ## login  
    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

#   def signup(self):
#     print(request.form)

#     # Create the user object
#     user = {
#       "_id": uuid.uuid4().hex,
#       "name": request.form.get('name'),
#       "email": request.form.get('email'),
#       "password": request.form.get('password')
#     }

#     # Encrypt the password
#     user['password'] = pbkdf2_sha256.encrypt(user['password'])

#     # Check for existing email address
#     if db.users.find_one({ "email": user['email'] }):
#       return jsonify({ "error": "Email address already in use" }), 400

#     if db.users.insert_one(user):
#       return self.start_session(user)

#     return jsonify({ "error": "Signup failed" }), 400
  
    def signout(self):
        session.pop('username', None)
        return redirect('/')
  
    def login(self):
        user = db.users.find_one({'username': request.form['username']})
    
        # if user and pbkdf2_sha256.verify(request.form['password'], user['password']):
        #   return self.start_session(user)
        if user and user['password'] == request.form['password']:
            session['username'] = request.form['username']
            if user['role'] == 'Admin':
                return redirect(url_for('admin'))
            elif user['role'] == 'Bác sĩ':
                return redirect(url_for('doctor'))
            else:
                return redirect(url_for('patient'))
        else:
            error = "Không tồn tại tài khoản này"
            return render_template('index.html', error = error)
    
    def register(self):
        user = {
            'name': request.form['name'],
            'username': request.form['username'],
            'password': request.form['password'],
            'email': request.form.get('email'),
            'urlnhiptho': request.form.get('urlnhiptho'),
            'urltiengho': request.form.get('urltiengho'),
            'urltiengwheeze': request.form.get('urltiengwheeze'),
            'urltiengrale': request.form.get('urltiengrale'),
            'urltienggay': request.form.get('urltienggay'),
            'address': request.form.get('address'),
            'role': request.form.get('role'),
            'gender': request.form.get('gender'),
            'phone': request.form.get('phone')
        }
        insertUser = db.users.insert_one(user)
        flash("Đăng kí thành công!")
        return redirect("/")

    ## CRUD User

    def addUser(self):
        user = {
            'name': request.form['name'],
            'username': request.form['username'],
            'password': request.form['password'],
            'email': request.form.get('email'),
            'urlnhiptho': request.form.get('urlnhiptho'),
            'urltiengho': request.form.get('urltiengho'),
            'urltiengwheeze': request.form.get('urltiengwheeze'),
            'urltiengrale': request.form.get('urltiengrale'),
            'urltienggay': request.form.get('urltienggay'),
            'address': request.form.get('address'),
            'role': request.form.get('role'),
            'gender': request.form.get('gender'),
            'phone': request.form.get('phone')
        }
        insertUser = db.users.insert_one(user)
        return redirect('admin')

    def deleteUser(self, username):
        db.users.delete_one({'username': username})
        return redirect(url_for('admin'))
    
    def updateUser(self, username):
        db.users.update_one(
            {"username": username}, 
            {"$set": {
                'urlnhiptho': request.form.get('urlnhiptho'),
                'urltiengho': request.form.get('urltiengho'),
                'urltiengwheeze': request.form.get('urltiengwheeze'),
                'urltiengrale': request.form.get('urltiengrale'),
                'urltienggay': request.form.get('urltienggay'),
                'address': request.form.get('address'),
                'phone': request.form.get('phone')}
            }
        )
        return redirect(url_for('admin'))
    
