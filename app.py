from flask import Flask, render_template, request, redirect, url_for, session
from user.models import User, db
import bcrypt
from xlwt import Workbook 

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
    'static',
    'register'
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
    username = session['username']
    if request.method == 'GET':
        return render_template('adduser.html', name=username)
    else:
        return User().addUser()

@app.route('/dashboard', methods=['GET'])
def dashboard():
    username = session['username']
    userInfo = db.users.find_one({
        'username': username
    })
    if userInfo['role'] == 'Admin':
        users = db.users.find({})
        return render_template('dashboard.html', users = users, name=username)
    elif userInfo['role'] == 'Bác sĩ':
        patients = db.users.find({
            'role': 'Bệnh nhân'
        })
        return render_template('doctor.html', patients = patients, name=username)
    else:
        user = db.users.find_one({
            'username': username
        })
        return render_template('patient.html', user = user, name=username)

@app.route('/user_profile/<username>', methods=['GET', 'POST']) # xem profile bệnh nhân và update user profile
def user_profile(username):
    user = db.users.find_one({
        'username': username
    })
    name = db.users.find_one({
        'username': session['username']
    })
    if request.method == 'GET':
        return render_template('user_profile.html', user=user, name=name)
    if request.method == 'POST':
        return User().updateUserProfile(username)

@app.route('/report/<username>', methods=['GET', 'POST']) 
def report_patient(username):
    name = db.users.find_one({
        'username': session['username']
    })
    user = db.users.find_one({
        'username': username
    })
    if request.method == 'GET':
        return render_template('report_cough.html', user=user, name=name, username=username)
    if request.method == 'POST':
        return User().updateUserReport(username)
        
@app.route('/<tenloaigiamsat>/<username>', methods=['GET']) #link xem url của bệnh nhân
def urlPatient(tenloaigiamsat, username):
    name=session['username']
    user_url = db.users.find_one({ #
        'username': username
    })
    print(tenloaigiamsat+"/n=========")
    url = None
    if tenloaigiamsat in ['nhiptho','tiengho','tiengwheeze','tiengrale','tiengngay']:
        if user_url['url'+tenloaigiamsat] is not None:
            url=str(user_url['url'+tenloaigiamsat])
    users_patient = db.users.find({
        'role': 'Bệnh nhân'
    })
    print(tenloaigiamsat+"/n=========")
    loaigiamsat = {
        'nhiptho': 'Nhịp thở',
        'tiengho': 'Tiếng ho',
        'tiengwheeze': 'Tiếng khò khè',
        'tiengrale': 'Tiếng rale',
        'tiengngay': 'Tiếng ngáy',
    }
    if tenloaigiamsat in loaigiamsat:
        return render_template('urlbenhnhan.html', tenloaigiamsat=tenloaigiamsat, username=username, giamsat=loaigiamsat, users=users_patient, url=url, user_url=user_url, name=name)

@app.route('/delete/<username>', methods=['GET'])
def delete_user(username):
    return User().deleteUser(username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        return User().register()

@app.route('/report', methods=['GET'])
def report():
    name = db.users.find_one({
        'username': session['username']
    })
    users = db.users.find({
        'role': 'Bệnh nhân'
    })
    loaigiamsat = {
        'nhiptho': 'Nhịp thở',
        'tiengho': 'Tiếng ho',
        'tiengwheeze': 'Tiếng khò khè',
        'tiengrale': 'Tiếng rale',
        'tiengngay': 'Tiếng ngáy',
    }
    wb = Workbook() 
    # add_sheet is used to create sheet. 
    sheet1 = wb.add_sheet('Báo cáo') 
    sheet1.write(0,0,'STT')
    sheet1.write(0,1,'Mã số bệnh nhân')
    sheet1.write(0,2,'Họ và tên')
    sheet1.write(0,3,'Giới tính')
    sheet1.write(0,4,'Khoa')
    sheet1.write(0,5,'Ngày nhập viện')
    index, row= 0,0
    for user in users:
        index+=1
        row+=1
        sheet1.write(row,0,index)
        if('id' in user):
            sheet1.write(row,1,user['id'])
        else:
            sheet1.write(row,1," ")
        sheet1.write(row,2,user['name'])
        if('gender' in user):
            sheet1.write(row,3,user['gender'])
        else:
            sheet1.write(row,3," ")
        if('department' in user):
            sheet1.write(row,4,user['department'])
        else:
            sheet1.write(row,4," ")
        if('dayPatient' in user):
            sheet1.write(row,5,user['dayPatient'])
        else:
            sheet1.write(row,5," ")
        wb.save('./static/Report.xls')
    if request.method == 'GET':
        users = db.users.find({
            'role': 'Bệnh nhân'
        })
        return render_template('report.html', giamsat=loaigiamsat, users=users, name=name)

@app.route('/giamsat/<tenloaigiamsat>', methods=['GET'])
def giamsat(tenloaigiamsat):
    name = db.users.find_one({
        'username': session['username']
    })
    users = db.users.find({
        'role': 'Bệnh nhân'
    })
    print(users)
    loaigiamsat = {
        'nhiptho': 'Nhịp thở',
        'tiengho': 'Tiếng ho',
        'tiengwheeze': 'Tiếng khò khè',
        'tiengrale': 'Tiếng rale',
        'tiengngay': 'Tiếng ngáy',
    }
    tengiamsat = None
    if tenloaigiamsat in loaigiamsat:
        tengiamsat = tenloaigiamsat
        return render_template('giamsat.html', giamsat = loaigiamsat, users = users, tenloaigiamsat = tenloaigiamsat, name=name)

@app.route("/signout")
def signout():
    return User().signout()

if __name__ == '__main__':
    app.run(port=8009, debug=True)