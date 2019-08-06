from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func
# from flask.ext.sqlalchemy import SQLAlchemy

app=Flask(__name__)
#connect to ur local database
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:taiwo@localhost/height_collector'
#connect to ur heroku db
app.config['SQLALCHEMY_DATABASE_URI']='postgres://tmwtcdjbfibbik:701e39a32f4b7da55f483ece8a45e5fd9e7d7f84ab5bf19897009e8efdd30a1a@ec2-107-20-168-237.compute-1.amazonaws.com:5432/d71akun90fb06c?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['MASTER_PASSWORD_REQUIRED'] = False

#create sqlalchemy object for your flask app
db=SQLAlchemy(app)

#create a model for the database
class Data(db.Model):
    __tablename__="data" #create table
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    height_=db.Column(db.Integer)

    #initialized the variable of your object created
    def __init__(self,email_,height_):
        self.email_=email_
        self.height_=height_

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/success/', methods=['POST'])
def success():
    #to capture the values when submit button is pressed.
    if request.method=='POST':
        email=request.form["email"] #to get email values entered
        height=request.form["height"] #to get height value entered
        # send_email(email,height)
        #validate data in the database(check for duplicate)
        if db.session.query(Data).filter(Data.email_==email).count()==0:
            data=Data(email,height)
            #create a session to add data to database
            db.session.add(data)
            #commit the changes
            db.session.commit()
            #calculate average height
            average_height=db.session.query(func.avg(Data.height_)).scalar()
            average_height=round(average_height,1)
            # print(average_height)
            #count all height
            count=db.session.query(Data.height_).count()
            send_email(email,height, average_height, count)
            #print(request.form)
            return render_template("success.html")
    return render_template("index.html",
    text="email already exist, try again!")

if __name__ == '__main__':
    app.debug=True
    app.run(port=5001)
