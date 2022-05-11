import os

import boto3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from photo_upload_service import photo_upload_service


# constants
HOST=os.getenv('HOST')
PORT=os.getenv('PORT')
DB_NAME=os.getenv('DB_NAME')
USER=os.getenv('USER')
PASSWORD=os.getenv('PASSWORD')


# create and configure the app db
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}'
db = SQLAlchemy(app)


# register services
app.register_blueprint(photo_upload_service.blueprint)


# create and configure the app S3
app.config['S3_BUCKET'] = os.getenv('S3_BUCKET')
app.config['AWS_ACCESS_KEY'] = os.getenv('AWS_ACCESS_KEY')
app.config['AWS_SECRET_ACCESS_KEY'] = os.getenv('AWS_SECRET_ACCESS_KEY')

s3 = boto3.resource('s3')


# models
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    photos = db.relationship('PhotoMetadata', backref='user', lazy=True)

    def __repr__(self) -> str:
        return f'{self.user_id}: {self.username}'


class PhotoMetadata(db.Model):
    __tablename__ = 'photo_metadata'
    photo_id = db.Column(db.Integer, primary_key=True)
    photo_url = db.Column(db.String(300), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    def __repr__(self) -> str:
        return f'{self.photo_id}: {self.photo_url}'


# simple page that says hello
@app.route('/')
def hello():
    return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run()
