from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'dictCursor'

mysql = MySQL()

Articles = Articles()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id = id)
class RegisterForm(Form):
    name = StringField('Name', validators=[validators.length(min = 1, max = 50)])
    username  = StringField('Username', validators=[validators.length(min = 4, max = 25)])
    email  = StringField('Email', validators=[validators.length(min = 6, max = 50)])
    password  = PasswordField('Password', validators=[
    validators.data_required(),
    validators.EqualTo('Confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm password')

@app.route("/register", methods= ['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        return render_template('register.html')
    return render_template('register.html', form=form)

#create cursor
cur = mysql.connection.cursor()
cur.execute("INSERT INTO users(name, email, username, password) VALUES (%s,%s,%s,%s)", (name,email,username,password))
#commit to DB
mysql.connection.commit()
#close connection
cur.close()
flash('You are now registered and can log in', 'success')
redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug = True)
