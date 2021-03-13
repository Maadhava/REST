from flask import Flask,request,jsonify,redirect
import json
import sqlite3
app=Flask(__name__)
app.secret_key="slvnsvdkcdvdf"
conn = sqlite3.connect('rest.db')
command1 = """CREATE TABLE IF NOT EXISTS
user(email TEXT ,password TEXT,s TEXT)"""
cursor = conn.cursor()
cursor.execute(command1)
@app.route('/')
@app.route('/rest/api/signup',methods=['POST'])
def signup():
    if request.method=='POST':
        email=request.json['email']
        password=request.json['password']
        conn = sqlite3.connect('rest.db')
        cursor=conn.cursor()
        s="True"
        cursor.execute("SELECT email from user WHERE email=?",(email,))
        r=cursor.fetchall()
        if len(r)==0:
            cursor.execute("INSERT INTO user VALUES(?,?,?)",(email,password,s))
            conn.commit()
            cursor.execute("SELECT * FROM user WHERE email=email and password=password")
            res=cursor.fetchall()
            return jsonify(res)
        else:
            return "User exists!"
@app.route('/rest/api/signin',methods=['POST'])
def signin():
    if request.method=='POST':
        email=request.json['email']
        password=request.json['password']
        conn=sqlite3.connect('rest.db')
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM user WHERE email=? and password=?",(email,password))
        res={}
        r=[]
        r=cursor.fetchall()
        if(len(r)==1):
            cursor.execute("UPDATE user set s=? WHERE email=?",("True",email))
            conn.commit()
            cursor.execute("SELECT * FROM user WHERE email=? and password=?",(email,password))
            res=cursor.fetchall()
            return jsonify(res)
        else:
            return "User does not exists!"
@app.route('/rest/api/logout',methods=['POST'])
def logout():
    if request.method=='POST':
        email=request.json['email']
        password=request.json['password']
        conn=sqlite3.connect('rest.db')
        cursor=conn.cursor()
        cursor.execute("UPDATE user set s=? WHERE email=?",("False",email))
        conn.commit()
        cursor.execute("SELECT * FROM user WHERE email=?",(email,))
        r=cursor.fetchall()
        return jsonify(r)
@app.route('/rest/api/delete',methods=['DELETE'])
def delete():
    if request.method=='DELETE':
        email=request.json['email']
        password=request.json['password']
        conn=sqlite3.connect('rest.db')
        cursor=conn.cursor()
        cursor.execute("SELECT email from user where email=?",(email,))
        r=cursor.fetchall()
        if(len(r)==1):
            cursor.execute("DELETE from user WHERE email=?",(email,))
            conn.commit()
            return "user deleted"
        else:
            return "user doesnt exists"
@app.route('/rest/api/forgotpassword',methods=['POST'])
def forgotpassword():
    if request.method=='POST':
        password=request.json['password']
        conn=sqlite3.connect('rest.db')
        cursor=conn.cursor()
        cursor.execute("UPDATE user set password=?",(password,))
        return "Password changed!"
if __name__=="__main__":
    app.debug=True
    app.run(host='localhost',port=5000)