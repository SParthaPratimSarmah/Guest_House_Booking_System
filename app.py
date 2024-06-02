import re
from flask import request
from flask import render_template, request, redirect, url_for, session
from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from model import db, User, Room, Bookings, Guest
from sqlalchemy import or_
from flask import Flask, render_template, request, redirect, url_for
from model import db, Guest


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/GuestBookingSystem2302021'
db.init_app(app)


def get_current_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@app.route("/logout")
def logout():
    # Clear the user session
    session.pop('username', None)
    session.pop('guestid', None)
    session.pop('bid', None)
    session.pop('roomtypeid', None)
    session.pop('roomid', None)
    return redirect(url_for('hello'))  # Redirect to the homepage


@app.route("/search_guest_id", methods=['POST'])
def search_guest_id():
    if request.method == 'POST':
        name = request.form.get('name')
        mobile = request.form.get('mobile')

        # Query the Guest table to find the guest by name and mobile number
        guest = Guest.query.filter_by(gname=name, gphone=mobile).first()

        if guest:
            guestid = guest.guestid

            # Query booking details based on the guestid
            booking_details = db.session.query(
                Bookings.bid,
                Bookings.guestid,
                Guest.gname,
                Bookings.roomtypeid,
                Bookings.from_,
                Bookings.to_,
                Bookings.roomid,
                Bookings.Check_out,
                Room.room_number,
                Room.room_flor,
                Bookings.status
            ).join(
                Guest, Bookings.guestid == Guest.guestid
            ).join(
                Room, Bookings.roomid == Room.roomid
            ).filter(
                Bookings.guestid == guestid
            ).all()

            return render_template("booking_details_table.html", guestid=guestid, booking_details=booking_details)
        else:
            return "Guest not found. Please check the name and mobile number."


@app.route("/")
def hello():
    return render_template("HomePage.html")


@app.route("/available_rooms", methods=['GET'])
def available_rooms():
    if 'guestid' in session:
        guestid = session['guestid']

        # Get the list of available rooms with status 'empty', 'canceled', or 'completed'
        available_rooms = Room.query.filter(
            Room.status.in_(['empty', 'canceled', 'completed'])).all()

        return render_template("available_rooms.html", available_rooms=available_rooms, guestid=guestid)
    else:
        return "User not logged in."


@app.route("/passwordrecovery")
def passwordrecovery():
    return render_template("passwordrecovery.html")


@app.route("/newentry")
def new():
    return render_template('recipHome.html')


@app.route("/Book_room")
def bookroom():
    return render_template('guestbook.html')


@app.route("/available_room")
def available_room():

    available_rooms = db.session.query(
        Bookings.bid,
        Bookings.guestid,
        Guest.gname,
        Bookings.roomtypeid,
        Bookings.from_,
        Bookings.to_,
        Bookings.roomid,
        Bookings.Check_out,
        Room.room_number,
        Room.room_flor,
        Room.status

    ).join(
        Guest, Bookings.guestid == Guest.guestid
    ).join(
        Room, Bookings.roomid == Room.roomid
    ).filter(
        Bookings.guestid == Bookings.guestid
    ).all()
    return render_template('roomavailability.html', available_rooms=available_rooms)


@app.route("/guestlist")
def guestlist():
    guests = Guest.query.all()  # Query all guests from the database
    return render_template('guestlist.html', guests=guests)


@app.route("/booking_details")
def booking_details():

    # Query booking details from the database based on guest ID
    booking_details = db.session.query(
        Bookings.bid,
        Bookings.guestid,
        Guest.gname,
        Bookings.roomtypeid,
        Bookings.from_,
        Bookings.to_,
        Bookings.roomid,
        Bookings.Check_out,
        Room.room_number,
        Room.room_flor,
        Bookings.status
    ).join(
        Guest, Bookings.guestid == Guest.guestid
    ).join(
        Room, Bookings.roomid == Room.roomid
    ).filter(
        Bookings.guestid == Bookings.guestid
    ).all()

    return render_template('booking_details.html', booking_details=booking_details)


@app.route("/search_book_details_here")
def search_book_details_here():
    # Query booking details from the database based on guest ID
    booking_details = db.session.query(
        Bookings.bid,
        Bookings.guestid,
        Guest.gname,
        Bookings.roomtypeid,
        Bookings.from_,
        Bookings.to_,
        Bookings.roomid,
        Bookings.Check_out,
        Room.room_number,
        Room.room_flor,
        Bookings.status
    ).join(
        Guest, Bookings.guestid == Guest.guestid
    ).join(
        Room, Bookings.roomid == Room.roomid
    ).filter(
        Bookings.guestid == Bookings.guestid
    ).all()

    return render_template('searchbookingdetails.html', booking_details=booking_details)


@app.route("/guestregister", methods=['GET', 'POST'])
def guestregister():
    if request.method == 'POST':
        # Get form data
        username = request.form['gusername']
        phone = request.form['phone']
        email = request.form['email']

        # Server-side validation
        if not username[0].isalpha():
            return "Username must start with a letter."

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return "Enter a valid email address."

        if not re.match(r"^\d{10}$", phone):
            return "Phone number must be 10 digits."

        # Check if a guest with the same details already exists
        existing_guest = Guest.query.filter_by(
            gname=username, gphone=phone, gemail=email).first()

        if existing_guest:
            return "A guest with the same details already exists."

        # If no existing guest is found, add the new user to the database
        new_user = Guest(gname=username, gphone=phone, gemail=email)

        try:
            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            # Store the guestid in the session
            session['guestid'] = new_user.guestid
            session['username'] = username

            # Redirect to the 'booking_request' route
            return redirect(url_for("booking_request"))
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {str(e)}"
    else:
        return render_template("Register.html")


@app.route("/codetails")
def codedetails():
    return render_template('contactdetails.html')


@app.route("/conBook", methods=['GET', 'POST'])
def conB():
    if request.method == 'POST':
        bid = session.get('bid')
        roomtypeid = session.get('roomtypeid')
        guestid = session.get('guestid')
        roomid = session.get('roomid')

        # Check if the selected room is available

        selected_room = Room.query.filter(
            Room.roomid == roomid,
            Room.status.in_(['empty', 'canceled', 'completed'])
        ).first()

        # selected_room = Room.query.filter_by(roomid=roomid, status='empty').first()

        if selected_room:
            booking = Bookings.query.get(bid)
            booking.roomid = roomid
            booking.status = '1'
            selected_room.status = 'booked'

            try:
                db.session.commit()
                return render_template("guestbook.html")
            except Exception as e:
                db.session.rollback()
                return f"An error occurred: {str(e)}"
        else:
            return "Invalid room selection. Please try again or select an available room"
    else:
        bid = session.get('bid')
        roomtypeid = session.get('roomtypeid')
        guestid = session.get('guestid')
        roomid = session.get('roomid')
        return render_template("guestconfirmed.html", bid=bid, roomtypeid=roomtypeid, roomid=roomid, guestid=guestid)


@app.route("/guq", methods=['GET', 'POST'])
def guq():
    if request.method == 'POST':
        if 'guestid' in session:
            guestid = session['guestid']
            # Separate roomtypeid field
            roomtypeid = request.form.get('roomtypeid')
            roomid = request.form.get('roomid')  # Separate roomid field
            from_date = request.form.get('from')
            to_date = request.form.get('to')
            from_date = datetime.strptime(from_date, '%Y-%m-%d')
            to_date = datetime.strptime(to_date, '%Y-%m-%d')

            if from_date > to_date:
                return "Invalid date range."

            new_booking = Bookings(
                guestid=guestid,
                roomtypeid=roomtypeid,  # Use the separate roomtypeid field
                from_=from_date,
                to_=to_date,
                roomid=roomid,  # Use the separate roomid field
                status="0",

            )

            try:
                db.session.add(new_booking)
                db.session.commit()

                bid = new_booking.bid
                guestid = new_booking.guestid

                # Get the list of available rooms with status 'empty'

                available_rooms = Room.query.filter(
                    Room.status.in_(['empty', 'canceled', 'completed'])).all()

                session['bid'] = bid
                session['roomtypeid'] = roomtypeid
                session['guestid'] = guestid
                session['roomid'] = roomid

                return redirect(url_for("conB", roomid=roomid, bid=new_booking.bid, roomtypeid=roomtypeid))
            except Exception as e:
                db.session.rollback()
                return f"An error occurred: {str(e)}"
    else:
        bid = session.get('bid')
        roomtypeid = session.get('roomtypeid')
        guestid = session.get('guestid')

        available_rooms = Room.query.filter(
            Room.status.in_(['empty', 'canceled', 'completed'])).all()

        return render_template("guestrequest.html", available_rooms=available_rooms, bid=bid, roomtypeid=roomtypeid, guestid=guestid)


@app.route("/gregister", methods=['GET', 'POST'])
def gregister():
    if request.method == 'POST':
        # Get form data
        username = request.form['gusername']
        phone = request.form['phone']
        email = request.form['email']

        # Server-side validation
        if not username[0].isalpha():
            return "Username must start with a letter."

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return "Enter a valid email address."

        if not re.match(r"^\d{10}$", phone):
            return "Phone number must be 10 digits."

        # Check if a guest with the same details already exists
        existing_guest = Guest.query.filter_by(
            gname=username, gphone=phone, gemail=email).first()

        if existing_guest:
            return "A guest with the same details already exists."

        # If no existing guest is found, add the new user to the database
        new_user = Guest(gname=username, gphone=phone, gemail=email)

        try:
            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            # Store the guestid in the session
            session['guestid'] = new_user.guestid
            session['username'] = username

            # Redirect to the 'booking_request' route
            return redirect(url_for("guq"))
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {str(e)}"
    else:
        return render_template("Register.html")


@app.route("/bookingrequest", methods=['GET', 'POST'])
def booking_request():
    if request.method == 'POST':
        if 'guestid' in session:
            guestid = session['guestid']
            # Separate roomtypeid field
            roomtypeid = request.form.get('roomtypeid')
            roomid = request.form.get('roomid')  # Separate roomid field
            from_date = request.form.get('from')
            to_date = request.form.get('to')
            from_date = datetime.strptime(from_date, '%Y-%m-%d')
            to_date = datetime.strptime(to_date, '%Y-%m-%d')

            if from_date > to_date:
                return "Invalid date range."

            new_booking = Bookings(
                guestid=guestid,
                roomtypeid=roomtypeid,  # Use the separate roomtypeid field
                from_=from_date,
                to_=to_date,
                roomid=roomid,  # Use the separate roomid field
                status="0",

            )

            try:
                db.session.add(new_booking)
                db.session.commit()

                bid = new_booking.bid
                guestid = new_booking.guestid

                # Get the list of available rooms with status 'empty'

                available_rooms = Room.query.filter(
                    Room.status.in_(['empty', 'canceled', 'completed'])).all()

                session['bid'] = bid
                session['roomtypeid'] = roomtypeid
                session['guestid'] = guestid
                session['roomid'] = roomid

                return redirect(url_for("book_confirmed", roomid=roomid, bid=new_booking.bid, roomtypeid=roomtypeid))
            except Exception as e:
                db.session.rollback()
                return f"An error occurred: {str(e)}"
    else:
        bid = session.get('bid')
        roomtypeid = session.get('roomtypeid')
        guestid = session.get('guestid')

        available_rooms = Room.query.filter(
            Room.status.in_(['empty', 'canceled', 'completed'])).all()

        return render_template("bookingrequest.html", available_rooms=available_rooms, bid=bid, roomtypeid=roomtypeid, guestid=guestid)


@app.route("/bookconfirmed", methods=['GET', 'POST'])
def book_confirmed():
    if request.method == 'POST':
        bid = session.get('bid')
        roomtypeid = session.get('roomtypeid')
        guestid = session.get('guestid')
        roomid = session.get('roomid')

        # Check if the selected room is available

        selected_room = Room.query.filter(
            Room.roomid == roomid,
            Room.status.in_(['empty', 'canceled', 'completed'])
        ).first()

        # selected_room = Room.query.filter_by(roomid=roomid, status='empty').first()

        if selected_room:
            booking = Bookings.query.get(bid)
            booking.roomid = roomid
            booking.status = '1'
            selected_room.status = 'booked'

            try:
                db.session.commit()
                return render_template("Congratulation.html")
            except Exception as e:
                db.session.rollback()
                return f"An error occurred: {str(e)}"
        else:
            return "Invalid room selection. Please try again or select an available room"
    else:
        bid = session.get('bid')
        roomtypeid = session.get('roomtypeid')
        guestid = session.get('guestid')
        roomid = session.get('roomid')
        return render_template("bookingconfirmedandcanceled.html", bid=bid, roomtypeid=roomtypeid, roomid=roomid, guestid=guestid)


@app.route("/recovery", methods=['POST'])
def recovery():
    if request.method == 'POST':
        username = request.form['uname']
        email = request.form['email']
        phone = request.form['phone']
        recovery_password = request.form['recovery_password']
        date_of_birth = request.form['age']

        user = User.query.filter_by(
            username=username, email=email, phone=phone, date_of_birth=date_of_birth).first()

        if user:
            hashed_recovery_password = bcrypt.generate_password_hash(
                recovery_password).decode('utf-8')
            user.password = hashed_recovery_password
            db.session.commit()
            return redirect(url_for('login'))
        else:
            print("User not found.")
        return redirect(url_for('passwordrecovery'))

    return render_template("passwordrecovery.html")


@app.route("/recip_home/<username>")
def recip_home(username):
    if 'username' in session:
        return render_template("recipHome.html", username=username)
    else:
        return "User not logged in."


@app.route("/guesthome/<username>")
def guest_home(username):
    if 'username' in session:
        return render_template("guesthome.html", username=username)
    else:
        return "User not logged in."


@app.route("/room_details_login_guest")
def room_details_login_guest():
    if 'username' in session:
        # Get the list of available rooms with status 'empty', 'canceled', or 'completed'
        available_rooms = Room.query.filter(
            Room.status.in_(['empty', 'canceled', 'completed'])).all()
        return render_template("guestavailable.html", available_rooms=available_rooms)
    else:
        return "User not logged in."


@app.route("/available_room_details")
def room_details_():
    if 'username' in session:
        # Get the list of available rooms with status 'empty', 'canceled', or 'completed'
        available_rooms = Room.query.filter(
            Room.status.in_(['empty', 'canceled', 'completed'])).all()
        return render_template("recipavailableroomdetails.html", available_rooms=available_rooms)
    else:
        return "User not logged in."


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_type = request.form.get('userType')

        if not username[0].isalpha():
            return render_template("Login.html", error="Username must start with a letter.")

        user = User.query.filter_by(username=username).first()

        if user:
            if bcrypt.check_password_hash(user.password, password):
                if user.Type == user_type:
                    session['username'] = username
                    if user_type == 'Receptionist':
                        return redirect(url_for('recip_home', username=username))
                    elif user_type == 'Guest':
                        return redirect(url_for('guest_home', username=username))
                else:
                    return render_template('Login.html', error="You are not authorized to access this user type.")
            else:
                return render_template('Login.html', error="Incorrect password. Please try again.")
        else:
            return render_template('Login.html', error="User not found. Please register.")

    return render_template("Login.html")


@app.route("/BookCANCEL", methods=['POST'])
def BookCANCEL():
    if request.method == 'POST':
        bid = request.form['bid']

        # Find the booking based on bid
        booking = Bookings.query.get(bid)

        if booking:
            # Update the booking status to 2 (canceled)
            booking.status = '2'

            # Find the room associated with the booking
            room = Room.query.get(booking.roomid)

            if room:
                # Update the room status to 'canceled'
                room.status = 'canceled'

            try:
                db.session.commit()
                return render_template('guestbook.html')
            except Exception as e:
                db.session.rollback()
                return f"An error occurred: {str(e)}"
        else:
            return "Booking not found."
    return render_template('guestbook.html')


@app.route("/cancel_booking", methods=['POST'])
def cancel_booking():
    if request.method == 'POST':
        bid = request.form['bid']

        # Find the booking based on bid
        booking = Bookings.query.get(bid)

        if booking:
            # Update the booking status to 2 (canceled)
            booking.status = '2'

            # Find the room associated with the booking
            room = Room.query.get(booking.roomid)

            if room:
                # Update the room status to 'canceled'
                room.status = 'canceled'

            try:
                db.session.commit()
                return redirect(url_for('booking_details'))
            except Exception as e:
                db.session.rollback()
                return f"An error occurred: {str(e)}"
        else:
            return "Booking not found."
    return redirect(url_for('booking_details'))


@app.route("/check_in", methods=['POST'])
def checkin():
    if request.method == 'POST':
        bid = request.form['bid']
        booking = Bookings.query.get(bid)

        if booking:
            booking.status = '3'

            room = Room.query.get(booking.roomid)

            if room:
                room.status = 'occupied'

            try:
                db.session.commit()
                return redirect(url_for('booking_details'))
            except Exception as e:
                db.session.rollback()
                return f"An error occurred: {str(e)}"
        else:
            return "Booking not found."
    return redirect(url_for('booking_details'))


@app.route("/check_out", methods=['POST'])
def checkout():
    if request.method == 'POST':
        bid = request.form['bid']
        booking = Bookings.query.get(bid)

        if booking:
            booking.status = '4'
            booking.Check_out = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            room = Room.query.get(booking.roomid)

            if room:
                room.status = 'completed'

                # Update the checkout time in the booking

            try:
                db.session.commit()
                return redirect(url_for('booking_details'))
            except Exception as e:
                db.session.rollback()
                return f"An error occurred: {str(e)}"
        else:
            return "Booking not found."
    return redirect(url_for('booking_details'))


@app.route('/empty_room_occupied', methods=['POST'])
def empty_room_occupied():
    if request.method == 'POST':
        bid = request.form['bid']
        booking = Bookings.query.get(bid)

        if booking:
            booking.status = '0'
            booking.emptytime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            room = Room.query.get(booking.roomid)

            if room:
                room.status = 'empty'

                # Update the checkout time in the booking

            try:
                db.session.commit()
                return redirect(url_for('booking_details'))
            except Exception as e:
                db.session.rollback()
                return f"An error occurred: {str(e)}"
        else:
            return "Booking not found."
    return redirect(url_for('booking_details'))


@app.route("/confirmed", methods=['POST'])
def confirmed():
    if request.method == 'POST':
        bid = request.form['bid']

        # Find the booking based on bid
        booking = Bookings.query.get(bid)

        if booking:
            # Update the booking status to '1' (confirmed)
            booking.status = '1'

            # Find the room associated with the booking
            room = Room.query.get(booking.roomid)

            if room:
                # Update the room status to 'booked'
                room.status = 'booked'

            try:
                db.session.commit()
                # Redirect back to the booking details page
                return redirect(url_for('booking_details'))
            except Exception as e:
                db.session.rollback()
                return f"An error occurred: {str(e)}"
        else:
            return "Booking not found."

    return "Invalid request"


secret_code_file_path = 'secretcode.txt'


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        date_of_birth = request.form['age']
        user_type = request.form['userType']

        if not username[0].isalpha():
            return "Username must start with a letter."

        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')

        # Check if a user with the same username or email already exists
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            return "A user with the same username or email already exists."

        # Check the selected user type and insert the user into the Users table accordingly
        if user_type == 'Guest':
            new_user = User(username=username, password=hashed_password, email=email,
                            phone=phone, date_of_birth=date_of_birth, Type=user_type)
            # new_user2 = Guest(gname=username, gphone=phone, gemail=email)
            try:
                db.session.add(new_user)
                db.session.commit()
                # db.session.add(new_user2)
                # db.session.commit()
                return render_template("Login.html")
            except Exception as e:
                db.session.rollback()
                return f"An error occurred: {str(e)}"
        else:
            # If it's a receptionist, check the secret code
            secret_code = request.form['secret_code']
            with open(secret_code_file_path, 'r') as file:
                correct_secret_code = file.read().strip()
            if secret_code != correct_secret_code:
                return "Incorrect secret code. Registration failed."

            new_user = User(username=username, password=hashed_password, email=email,
                            phone=phone, date_of_birth=date_of_birth, Type=user_type)
            try:
                db.session.add(new_user)
                db.session.commit()
                return render_template("Login.html")
            except Exception as e:
                db.session.rollback()
                return f"An error occurred: {str(e)}"
    else:
        return render_template("Register.html")


if __name__ == '__main__':
    app.run(debug=True)
