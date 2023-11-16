from better_profanity import profanity
from flask import Flask,render_template,request,redirect,url_for,session,flash
import mysql.connector
import os
import json
import numpy as np
import pandas as pd

import datetime

df = pd.read_csv('cyberbullying_tweets.csv')

json_data = df.to_json(orient='index')

with open('Dataset.json', 'w') as f:
    f.write(json_data)

UPLOAD_FOLDER = 'static/file/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

mydb = mysql.connector.connect(host="localhost",user="root",password="",database="cyber")
mycursor = mydb.cursor(buffered=True)



@app.route('/')
def login():
    return render_template('login.html')


@app.route('/loginpost.html', methods = ['POST','GET'])
def userloginpost():
    global data1
    if request.method == 'POST':
        data1 = request.form.get('username')
        data2 = request.form.get('password')

        sql = "SELECT * FROM `users` WHERE `name` = %s AND `password` = %s"
        val = (data1, data2)
        mycursor.execute(sql,val)
        account = mycursor.fetchone()
        if account:
            uname = data1

            return render_template('snipe.html', uname=uname)
        elif data1 == 'Admin' and data2 == 'Admin':
            sql = 'SELECT * FROM `tweets`'
            mycursor.execute(sql)
            result = mycursor.fetchall()
            if result:
                sql2 = 'SELECT * FROM `tweets`'
                mycursor.execute(sql2)
                account1 = mycursor.fetchall()


                return render_template('tweet.html', data=account1)
            return render_template('tweet.html', msg='No tweets')
            #return render_template('tweet.html')
        else:
            return render_template('login.html',msg = 'Invalid')
@app.route('/pages-register.html')
def reg():
    return render_template('pages-register.html')
@app.route('/back')
def back():
    uname = data1
    return render_template('twitter.html', uname=uname)

@app.route('/reg',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        name = request.form.get('username')
        phone = request.form.get('phone')
        password = request.form.get('password')
        sql = "INSERT INTO users (`name`, `phone`, `password`) VALUES (%s, %s, %s)"
        val = (name,phone,password)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('login.html')

@app.route('/send',methods=['POST','GET'])
def send():
    if request.method == 'POST':

        msg = request.form.get('msg')
        censored = profanity.censor(msg)


        if '*' in censored:
            uname = data1
            flash("Hello user! You send wrong word Please Change it!")
            return render_template('snipe.html',uname=uname,view = 'style=display:block', value = 'Hello user! You send wrong word Please Change it!')
        else:

            now = datetime.datetime.now()
            sql = "INSERT INTO `tweets` (`name`, `date`, `tweet`) VALUES (%s, %s, %s)"
            val = (data1, now, msg)
            mycursor.execute(sql, val)
            mydb.commit()
            uname = data1
            sql2 = 'SELECT id FROM `tweets`'
            mycursor.execute(sql2)
            account = mycursor.fetchall()
            v = len(account)
            print(v)
            sql = "SELECT * FROM `tweets` WHERE `id` = %s"
            val1 = (v,)
            mycursor.execute(sql,val1)
            result = mycursor.fetchall()
            sql3= 'SELECT name,tweet FROM `tweets`'
            mycursor.execute(sql3)
            rows = mycursor.fetchall()
            row_counter = 0
            chunked_rows = [rows[i:i + 10] for i in range(0, len(rows), 10)]



            return render_template('snipe.html',uname=uname,rows=rows, row_counter=row_counter)


@app.route('/tweet')
def tweet():
    sql = 'SELECT * FROM `tweets`'
    mycursor.execute(sql)
    result = mycursor.fetchall()
    if result:
        return render_template('tweet.html', data = result)
    return render_template('tweet.html', msg = 'No tweets')


@app.route('/upload.html')
def up():
    return render_template('upload.html')



@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')


'''@app.route('/send',methods=['POST','GET'])
def send():
    if request.method == 'POST':

        msg = request.form.get('msg')
        censored = profanity.censor(msg)


        if '*' in censored:
            uname = data1
            flash("Hello user! You send wrong word Please Change it!")
            return render_template('snipe.html',uname=uname,view = 'style=display:block', value = 'Hello user! You send wrong word Please Change it!')
        else:

            now = datetime.datetime.now()
            sql = "INSERT INTO `tweets` (`name`, `date`, `tweet`) VALUES (%s, %s, %s)"
            val = (data1, now, msg)
            mycursor.execute(sql, val)
            mydb.commit()
            uname = data1
            sql2 = 'SELECT id FROM `tweets`'
            mycursor.execute(sql2)
            account = mycursor.fetchall()
            v = len(account)
            print(v)
            sql = "SELECT * FROM `tweets` WHERE `id` = %s"
            val1 = (v,)
            mycursor.execute(sql,val1)
            result = mycursor.fetchall()
            sql3= 'SELECT name,tweet FROM `tweets`'
            mycursor.execute(sql3)
            account1 = mycursor.fetchall()
            a1=[]
            b1=[]
            for sts in account1:
                a = sts[0]
                b = sts[1]
                print(a)
                a1.append(a)
                b1.append(b)
            a2 = len(a1)
            b2 = len(b1)
            n=''
            tw = ''
            ans =''
            chunked_rows = [rows[i:i + 10] for i in range(0, len(rows), 10)]

            for ans in range(a2):
                print(ans)
                n = a1[ans]
            for ans1 in range(b2):
                print(ans1)
                tw = b1[ans1]

            return render_template('snipe.html',uname=uname,data=account1)'''





if __name__ == '__main__':
    app.run(debug=True,port=2000)