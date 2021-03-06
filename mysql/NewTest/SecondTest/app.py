# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 17:00:04 2019

@author: user
"""

from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
#import yaml

app = Flask(__name__)

# Configure db
# db = yaml.load(open('Credentials.yaml'))

#Configuration by Billio
app.config['MYSQL_DATABASE_HOST'] = 'sql12.freemysqlhosting.net' 
app.config['MYSQL_DATABASE_USER'] = 'sql12280733' 
app.config['MYSQL_DATABASE_DB'] = 'sql12280733'

#Initialising the app
mysql = MySQL()
mysql.init_app(app)

@app.route('/', methods=['GET', 'POST']) #Both Methods Needed
def index():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        name = userDetails['name']
        password = userDetails['password']
        email = userDetails['email']
        
        cur = mysql.get_db().cursor()
        cur.execute("INSERT INTO Registration(id, Username, email, password_hash) VALUES(%s, %s, %s, %s)",("21", name, email,password))
        mysql.get_db().commit()
        #cur.close()
        return redirect('/') #after clicking submit it will go straight to expected place
    return render_template('index.html') #creating a typeform of username and email

#@app.route("/login")
#def login():
#	  return render_template("login1.html",title="data")
      
@app.route("/checkUser",methods=['GET', "POST"])
def check():
    if request.method == 'POST':
        userDetails = request.form
        logname = userDetails['name']
        logpassword = userDetails['password']
        cur = mysql.get_db().cursor()
        cur.execute("SELECT Username,password_hash FROM Registration WHERE '"+logname+"' = Username AND '"+logpassword+"' = password_hash")
        user = cur.fetchall()  
        
        if len(user) == 1 :
            return "SUCCESS"
#            return render_template('users.html',userDetails=userDetails)
        else:
            return "failed"
    return render_template("login1.html")
    
#@app.route('/users') #display the users
#def users():
#    cur = mysql.get_db().cursor()
#    resultValue = cur.execute("SELECT * FROM StartingNew")
#    if resultValue > 0:
#        userDetails = cur.fetchall()
#        return render_template('users.html',userDetails=userDetails)

if __name__ == '__main__':
    app.run(debug=True)