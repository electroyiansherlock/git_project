from os import name
from typing import AsyncGenerator
from flask import Flask, render_template, request, url_for, redirect, session
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    choice = db.Column(db.String(100))
    
    # It is important to set the default value of this session.
    
    def __init__(self, name = None, age = None, choice = None):
        self.name = name 
        self.age = age
        self.choice = choice
    
    def __repr__(self):
        return f'{self.id} - {self.name} - {self.choice} - {self.age}'
    

@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    
    if request.method == "POST" : 
        
        person_name = request.form.get('person')
        person_age = request.form.get('age')
        person_choice = request.form.get('selected')
        
        print("The name of the person is : ", end = " ")
        print(person_name)
        
        print("The age of the person is : ", end = " ")
        print(person_age)
        
        print("The choice of the person is : ", end = " ")
        print(person_choice)
        
        user1 = User()
        user1.name = person_name
        user1.age = person_age
        user1.choice = person_choice
        
        print("The values are : ")
        print(user1.name)
        print(user1.age)
        print(user1.choice)
        
        db.session.add(user1)
        db.session.commit()
        
        return redirect(url_for("users"))
    
    else : 
        return render_template('index.html')


@app.route('/users', methods = ['POST', 'GET'])
def users():
    all_users = User.query.all()
    
    print("inside the users url the USERS are : ")
    
    for auser in all_users :
        print(auser)
        
    return render_template('show.html')


if __name__ == "__main__":
    db.create_all()
    app.run(debug = True, port = 5000)