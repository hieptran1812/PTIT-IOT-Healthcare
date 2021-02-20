from flask import Flask, render_template, request, redirect, url_for, session
import database

def login():
    users = database.db.users
    login_user = users.find_one({'username': request.form['username']})
    if login_user:
        # if brcypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
        #     return true
        if request.form['password'] == login_user['password']:
            return str(login_user['role'])

def signout():
    session.clear()
    return redirect('/')    