import uuid, os
from flask import Flask, make_response, redirect, request, render_template, url_for
from flask_wtf.csrf import CSRFProtect
from model import db, User
from form import RegisterForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SECRET_KEY'] = 'you-will-never-guess'
csrf = CSRFProtect(app)
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def root():
    if not os.path.exists('./instance/mydatabase.db'):
        db.create_all()

    form = RegisterForm()
    print('qqq')
    if request.method == 'POST' and form.validate():
        name = form.name.data
        last_name = form.last_name.data
        email = form.email.data
        passwd = form.passwd.data
        salt = uuid.uuid4().hex
        hashed_password = hash(passwd + salt)
        user = User(name=name, last_name=last_name, email=email, passwd=hashed_password, salt=salt) 
        db.session.add(user)
        db.session.commit()
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run()