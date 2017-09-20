from flask import Flask, render_template, redirect, request, flash,session
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = "poptarts"
mysql = MySQLConnector(app, 'usersdb')
#print mysql.query_db("SELECT * FROM users")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/email', methods=['POST'])
def checkemail():
    # print "ksjdfhjksdhf"
    if len(request.form['email']) < 1:
        flash("email cannot be empty!")
        return redirect('/')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash('invalid input!')
    else:
        #print "EMAIL VALID"
        #flash('Valid!')
        query = 'SELECT * FROM users WHERE email = :email '
        data = {
            'email': request.form['email']
        }
        array = mysql.query_db(query, data)
        if len(array) < 1:

            query = 'INSERT INTO users(email) VALUES(:email);'


            data = {
                "email": request.form['email'],
            }
            mysql.query_db(query, data)
            #query = 'SELECT email FROM users'
            #array = mysql.query_db(query)
            #print array[0]['email']
            return redirect('/success')

        else:
            flash('This email is already taken!')
            return redirect('/')

@app.route('/success')
def success():
   query = "SELECT * FROM users;"
   all_users = mysql.query_db(query)
   return render_template('success.html', all_emails =  all_users )

app.run(debug=True)
