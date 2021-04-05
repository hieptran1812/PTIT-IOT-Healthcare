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
    def __init__(self):
        self.userProperties = {
            'name': request.form.get('name'),
            'username': request.form.get('username'),
            'password': request.form.get('password'),
            'email': request.form.get('email'),
            'urlnhiptho': request.form.get('urlnhiptho'),
            'urltiengho': request.form.get('urltiengho'),
            'urltiengwheeze': request.form.get('urltiengwheeze'),
            'urltiengrale': request.form.get('urltiengrale'),
            'urltiengngay': request.form.get('urltiengngay'),
            'address': request.form.get('address'),
            'role': request.form.get('role'),
            'gender': request.form.get('gender'),
            'phone': request.form.get('phone'),
            'note': request.form.get('note'),
            'inChargeDoctor': request.form.get('inChargeDoctor'),
            'job': request.form.get('job'),
            'dayPatient': request.form.get('dayPatient'),
            'symptom': request.form.get('symptom'),
            'birth': request.form.get('birth'),
            'id': request.form.get('id'),#mã số bệnh nhân
            'follow': request.form.get('follow'),#theo dõi từ ngày
            'researchStaff': request.form.get('researchStaff'),#cán bộ nghiên cứu
            'ethnicGroup': request.form.get('ethnicGroup'), #dân tộc
            'age': request.form.get('age'),
            'department': request.form.get('department'),#khoa
            'dayResearch': request.form.get('dayResearch'), #ngày thử nghiệm
            'cough': request.form.get('cough'), #Ho
            'breathing': request.form.get('breathing'), #nhịp Thở
            'wheeze': request.form.get('wheeze'), #thở khò khè
            'rale': request.form.get('rale'), #rale
            'snore': request.form.get('snore'), #ngáy
        }   
    ## login 
    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200
  
    def signout(self):
        session.pop('logged_in', None)
        return redirect('/')
  
    def login(self):
        user = db.users.find_one({'username': request.form.get('username')})
        if user and user['password'] == request.form.get('password'):
            session['logged_in'] = True
            session['username'] = request.form.get('username')
            return redirect('/dashboard')
        else:
            error = "Tên đăng nhập hoặc mật khẩu sai!"
            return render_template('index.html', error = error)
    
    def register(self):
        user = self.userProperties
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
        user = self.userProperties
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
        user = db.users.find_one({'username': username})
        flash('Đã xóa ' + str(user['role']).lower() + " " + str(user['name']) + "!")
        db.users.delete_one({'username': username})
        return redirect(url_for('dashboard'))
    
    def updateUserProfile(self, username): #update user in profile
        db.users.update_one(
            {"username": username}, 
            {"$set":
                {'urlnhiptho': request.form.get('urlnhiptho'),
                'urltiengho': request.form.get('urltiengho'),
                'urltiengwheeze': request.form.get('urltiengwheeze'),
                'urltiengrale': request.form.get('urltiengrale'),
                'urltiengngay': request.form.get('urltiengngay'),
                'address': request.form.get('address'),
                'gender': request.form.get('gender'),
                'phone': request.form.get('phone'),
                'note': request.form.get('note'),
                'job': request.form.get('job'),
                'dayPatient': request.form.get('dayPatient'),
                'symptom': request.form.get('symptom'),
                'birth': request.form.get('birth'),
                'id': request.form.get('id'),#mã số bệnh nhân
                'dayResearch': request.form.get('dayResearch'), #ngày thử nghiệm
            }}
        )
        flash('Cập nhật thành công!')
        return redirect('/user_profile/' + username)
    
    def updateUserReport(self, username): #update user in report
        # user={
        #     'name': request.form.get('name'),
        #     'address': request.form.get('address'),
        #     'gender': request.form.get('gender'),
        #     'note': request.form.get('note'),
        #     'dayPatient': request.form.get('dayPatient'),
        #     'id': request.form.get('id'),#mã số bệnh nhân
        #     'follow': request.form.get('follow'),#theo dõi từ ngày
        #     'researchStaff': request.form.get('researchStaff'),#cán bộ nghiên cứu
        #     'ethnicGroup': request.form.get('ethnicGroup'), #dân tộc
        #     'age': request.form.get('age'),
        #     'department': request.form.get('department'),#khoa
        #     'dayResearch': request.form.get('dayResearch'), #ngày thử nghiệm
        #     'cough': request.form.get('cough'), #Ho
        #     'breathing': request.form.get('breathing'), #nhịp Thở
        #     'wheeze': request.form.get('wheeze'), #thở khò khè
        #     'rale': request.form.get('rale'), #rale
        #     'snore': request.form.get('snore'), #ngáy
        user=self.userProperties
        userInDb = db.users.find_one({ # Tìm user trong database
            'username': user['username']
        })
        if userInDb:
            db.users.update_one(
                {"username": username}, 
                {"$set":
                    {
                        # 'gender': request.form.get('gender'),
                        # 'note': request.form.get('note'),
                        # 'dayPatient': request.form.get('dayPatient'),
                        # 'symptom': request.form.get('symptom'),
                        # 'birth': request.form.get('birth'),
                        # 'id': request.form.get('id'),#mã số bệnh nhân
                        # 'follow': request.form.get('follow'),#theo dõi từ ngày
                        # 'researchStaff': request.form.get('researchStaff'),#cán bộ nghiên cứu
                        # 'ethnicGroup': request.form.get('ethnicGroup'), #dân tộc
                        # 'age': request.form.get('age'),
                        # 'department': request.form.get('department'),#khoa
                        # 'dayResearch': request.form.get('dayResearch'), #ngày thử nghiệm
                        'cough.$': request.form.get('cough'), #Ho
                        # 'breathing': request.form.get('breathing'), #nhịp Thở
                        # 'wheeze': request.form.get('wheeze'), #thở khò khè
                        # 'rale': request.form.get('rale'), #rale
                        # 'snore': request.form.get('snore'), #ngáy
                    }
                }
            )
            flash('Cập nhật thành công!')
            return redirect('/report/' + username)
        else:
            insertUser = db.users.insert_one(user)
            flash("Thêm thông tin bệnh nhân thành công!")
            return render_template('report_cough.html')