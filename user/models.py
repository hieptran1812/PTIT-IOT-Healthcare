from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from passlib.hash import pbkdf2_sha256
from flask_pymongo import pymongo
import pandas as pd

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
        session.pop('logged_in', None)
        return redirect('/')
  
    def login(self):
        user = db.users.find_one({'username': request.form['username']})
       
        # if user and pbkdf2_sha256.verify(request.form['password'], user['password']):
        #   return self.start_session(user)
        if user and user['password'] == request.form['password']:
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect('/dashboard')
        else:
            error = "Tên đăng nhập hoặc mật khẩu sai!"
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
            'phone': request.form.get('phone'),
            'note': request.form.get('note')
        }
        userInDb = db.users.find_one({ # Tìm user trong database
            'username': user['username']
        })
        if userInDb:
            flash("Tên người dùng đã tồn tại!")
            return render_template('register.html')
        else:
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
            'phone': request.form.get('phone'),
            'relatives': request.form.get('relatives'),
            'relativePhone': request.form.get('relativePhone'),
            'note': request.form.get('note')
            # 'inChargeDoctor': request.form.get('inChargeDoctor')
        }
        userInDb = db.users.find_one({ # Tìm user trong database
            'username': user['username']
        })
        if userInDb:
            error = "Tên đăng nhập đã tồn tại!"
            return render_template('adduser.html', error = error)
        else:
            insertUser = db.users.insert_one(user)
            flash('Thêm người dùng thành công!')
            return redirect('adduser')

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
                'phone': request.form.get('phone'),
                'relatives': request.form.get('relatives'),
                'relativePhone': request.form.get('relativePhone'),
                # 'inChargeDoctor': request.form.get('inChargeDoctor')
                }
            }
        )
        flash('Cập nhật thành công!')
        return redirect('/user_profile/' + username)

# def exportExcel():
#     wb = Workbook() 
#     # add_sheet is used to create sheet. 
#     sheet1 = wb.add_sheet('Báo cáo') 
#     sheet1.write(0,0,'STT')
#     sheet1.write(0,1,'Tên đăng nhập')
#     sheet1.write(0,2,'Họ và tên')
#     sheet1.write(0,3,'Tần suất ho')
#     index, row= 0,1
#     for user in users:
#         index+=1
#         row+=1
#         sheet1.write(row,0,index)
#         sheet1.write(row,1,user['username'])
#         sheet1.write(row,2,user['name'])
#         sheet1.write(row,3,user['role'])
#     wb.save('Báo cáo.xls')
#     alert="Xuất file excel thành công!"
#     return render_template('report.html', alert=alert)
    
