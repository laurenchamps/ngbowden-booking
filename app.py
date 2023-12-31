from cs50 import SQL
from datetime import datetime, date
from flask import Flask, flash, redirect, render_template, request, session, jsonify, make_response
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import json

from helpers import apology, login_required, get_user_initial

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///ngbowden.db")


@app.route("/")
@login_required
def index():
    """Get user's current bookings"""
    myBookings = db.execute("SELECT * FROM events WHERE user_id=? AND date > datetime('now') ORDER BY date, start_time", session["user_id"])

    # Change date format to DD MMM YYYY for displaying on page
    for booking in myBookings:
        # Convert date to datetime object
        date_time = booking["date"] + ' ' + booking["start_time"]
        date_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M')

        booking["date"] = date_obj.strftime("%d %b %Y")

    # Get user's initial to display in navigation
    name = get_user_initial(db)

    # Get admin status of user
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    admin = user[0]["is_admin"]

    return render_template("index.html", bookings=myBookings, name=name, admin=admin)


@app.route("/book")
@login_required
def book():
    # Get user's initial to display in navigation
    name = get_user_initial(db)

    return render_template("book.html", name=name)


@app.route("/bookings")
@login_required
def bookings():

    # Provide access to page if user is admin
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

    if user[0]["is_admin"] == 1:
        # Get all future bookings for all users
        allBookings = db.execute("SELECT * FROM users JOIN events ON users.id = events.user_id WHERE date > datetime('now') ORDER BY date, start_time")

        # Change date format to DD MMM YYYY for displaying on page
        for booking in allBookings:
             # Convert date to datetime object
            date_time = booking["date"] + ' ' + booking["start_time"]
            date_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M')

            booking["date"] = date_obj.strftime("%d %b %Y")

        # Get user's initial to display in navigation
        name = get_user_initial(db)

        if len(allBookings) < 1:
            return render_template("bookings.html")

        return render_template("bookings.html", bookings=allBookings, name=name)
    
    else:
        return apology("You are not authorised to view this page", 403)


@app.route("/book/make-booking", methods=["GET", "POST"])
@login_required
def make_booking():

    if request.method == "POST":
        form_data = request.get_json()

        event_name = form_data["event_name"]
        date = form_data["date"]
        start_time = form_data["start_time"]
        end_time = form_data["end_time"]

        # Return error if any of the form fields are incomplete
        if not event_name or not date or not start_time or not end_time:
            response = make_response({"message": "Incomplete fields"}, 400)
            return response
        
        # Query database for an existing booking
        existing_bookings = db.execute("SELECT * FROM events WHERE date = ? AND ((start_time >= ? AND start_time < ?) OR (end_time > ? AND end_time <= ?))", date, start_time, end_time, start_time, end_time)

        # Convert date to datetime object
        date_time = date + ' ' + start_time
        date_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M')

        # Ensure date and start time is not in the past
        if date_obj < datetime.now():
            response = make_response({"message": "Your booking occurs in the past"}, 400)
            return response       

        # Return error if there is an existing booking at that time
        if len(existing_bookings) > 0:
            response = make_response({"message": "The booking time you have selected is unavailable"}, 400)
            return response
        
        # Add event to database
        rows = db.execute("INSERT INTO events (user_id, event_name, date, start_time, end_time) VALUES(?, ?, ?, ?, ?)",
            session["user_id"],
            event_name,
            date,
            start_time,
            end_time
        )

        response = make_response({"message": "Booking successful"}, 200)
        return response
    
    else:
        # If GET request, send details of all existing bookings to populate calendar
        events = db.execute("SELECT events.id, event_name, date, start_time, end_time, firstname, apartment FROM events JOIN users ON users.id = events.user_id ORDER BY start_time")

        response = make_response(jsonify(events), 200)

        return response


@app.route("/admin-delete", methods=["POST"])
@login_required
def admin_delete():

    # Remove booking
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM events WHERE id = ?", id)
    return redirect("/bookings")


@app.route("/user-delete", methods=["POST"])
@login_required
def user_delete():

    # Remove booking
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM events WHERE id = ?", id)
    return redirect("/")


@app.route("/edit-booking", methods=["GET", "POST"])
@login_required
def edit():

    if request.method == "POST":

        new_event_name = request.form.get("event-name")
        new_date = request.form.get("date")
        new_start_time = request.form.get("start-time")[:5]
        new_end_time = request.form.get("end-time")[:5]

        id = request.form.get("id")

        # Query database for an existing booking
        existing_bookings = db.execute("SELECT * FROM events WHERE date = ? AND ((start_time >= ? AND start_time < ?) OR (end_time > ? AND end_time <= ?))", new_date, new_start_time, new_end_time, new_start_time, new_end_time)

        # Return error if there is an existing booking at that time (that is not itself)
        if len(existing_bookings) > 0 and str(existing_bookings[0]["id"]) != id:
            response = make_response({"message": "The booking time you have selected is unavailable"}, 400)
            return response

        # Return error if any of the form fields are incomplete
        if not new_event_name or not new_date or not new_start_time or not new_end_time:
            response = make_response({"message": "Incomplete fields"}, 400)
            return response

        # Convert date to datetime object
        date_time = new_date + ' ' + new_start_time + ':00'
        date_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

        # Ensure date and start time is not in the past
        if date_obj < datetime.now():
            response = make_response({"message": "Your booking occurs in the past"}, 400)
            return response     

        # Update booking
        db.execute("UPDATE events SET event_name = ?, date = ?, start_time = ?, end_time = ? WHERE id = ?", new_event_name, new_date, new_start_time, new_end_time, id)

        return redirect("/")

    else:
        id = request.args.get("id")
        booking = db.execute("SELECT * FROM events WHERE id = ?", id)

        # Get values of existing event, convert to required format to pre-populate booking fields for editing
        date = booking[0]["date"]
        start_time = booking[0]["start_time"]
        start_time = f"{start_time}:00"
        end_time = booking[0]["end_time"]
        end_time = f"{end_time}:00"

        # Get user initial for displaying in navbar
        name = get_user_initial(db)

        return render_template("edit.html", booking=booking, date=date, start_time=start_time, end_time=end_time, name=name)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure email was submitted
        if not request.form.get("email"):
            return apology("Must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to homepage
        return redirect("/")

    # User reached route via GET (as by clicking a link or via a redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Register user"""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("password-confirmation")
        firstname = request.form.get("first-name")
        apartment = request.form.get("apartment")

        # Ensure first name is entered
        if not firstname:
            return apology("Enter a name", 400)

        # Ensure email is entered
        if not email:
            return apology("Enter an email", 400)

        # Ensure apartment is entered
        if not apartment:
            return apology("Enter your apartment number", 400)

        # Query database for email
        emails = db.execute("SELECT * FROM users WHERE email = ?", email)

        # Ensure username does not already exist
        if len(emails) > 0:
            return apology("Email address already in use", 400)

        # Ensure password is entered
        if not password:
            return apology("Enter a password", 400)

        # Ensure password and confirmation match
        if password != confirmation:
            return apology("Passwords do not match", 400)

        # Add user to database
        rows = db.execute("INSERT INTO users (email, firstname, apartment, hash) VALUES(?, ?, ?, ?)",
            email,
            firstname,
            apartment,
            generate_password_hash(password),
        )

        # Log user in and redirect to homepage
        user = db.execute("SELECT id FROM users WHERE email = ?", email)
        print(user[0]["id"])

        session["user_id"] = user[0]["id"]

        return redirect("/")

    else:
        return render_template("signup.html")
    

@app.route("/account")
@login_required
def account():
    # Get user details
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

    #  Get user initial to display in navbar
    name = get_user_initial(db)

    return render_template("account.html", user=user, name=name)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e - InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)