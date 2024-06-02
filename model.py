from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/GuestBookingSystem2302021'
db = SQLAlchemy(app)


class RoomType(db.Model):
    __tablename__ = 'roomtype'
    roomtypeid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roomtype_desc = db.Column(db.String(255), nullable=False)


class Room(db.Model):
    __tablename__ = 'rooms'
    roomid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_number = db.Column(db.String(255), nullable=False)
    room_flor = db.Column(db.Integer, nullable=False)  # Corrected column name
    roomtypeid = db.Column(db.Integer, db.ForeignKey(
        'roomtype.roomtypeid'), nullable=False)
    status = db.Column(db.String(255), nullable=False)

    roomtype = db.relationship('RoomType', backref='rooms')


class Guest(db.Model):
    __tablename__ = 'guests'
    guestid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gname = db.Column(db.String(255), nullable=False)
    gphone = db.Column(db.String(150), nullable=False)  # Corrected column name
    gemail = db.Column(db.String(255), nullable=False)


class Bookings(db.Model):
    __tablename__ = 'Bookings'
    bid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guestid = db.Column(db.Integer, db.ForeignKey(
        'guests.guestid'), nullable=False)
    roomtypeid = db.Column(db.Integer, db.ForeignKey(
        'roomtype.roomtypeid'), nullable=False)
    from_ = db.Column(db.DateTime, nullable=False)
    to_ = db.Column(db.DateTime, nullable=False)
    roomid = db.Column(db.Integer, db.ForeignKey(
        'rooms.roomid'), nullable=False)
    status = db.Column(db.String(255), nullable=False)
    Check_out = db.Column(db.DateTime, nullable=False)

    guest = db.relationship('Guest', backref='bookings')
    room = db.relationship('Room', backref='bookings')


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    Type = db.Column(db.String(255), nullable=False)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
