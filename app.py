""" Does this only relate to API from finance pset? So may not be required for my app 
import os """

from cs50 import SQL
from datetime import datetime, date
from flask import Flask, flash, redirect, render_template, request, session, jsonify, make_response
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import json

from helpers import apology, login_required

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
    """Show user's current bookings"""
    myBookings = db.execute("SELECT * FROM events WHERE user_id=?", session["user_id"])

    return render_template("index.html", bookings=myBookings)


@app.route("/book")
@login_required
def book():
    return render_template("book.html")


@app.route("/bookings")
def bookings():
    # Get all future bookings for all users
    allBookings = db.execute("SELECT * FROM users JOIN events ON users.id = events.user_id WHERE date > datetime('now') ORDER BY date, start_time")
    
    return render_template("bookings.html", bookings=allBookings)


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

        # Ensure date and start time is not in the past
        date_time = date + ' ' + start_time
        date_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M')

        if date_obj < datetime.now():
            response = make_response({"message": "Your booking occurs in the past"}, 400)
            return response       

        # Return error if there is an existing booking at that time
        if len(existing_bookings) > 0:
            response = make_response({"message": "The booking time you have selected is unavailable"}, 403)
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
        events = db.execute("SELECT events.id, event_name, date, start_time, end_time, firstname, apartment FROM events JOIN users ON users.id = events.user_id ORDER BY start_time")

        response = make_response(jsonify(events), 200)

        return response


@app.route("/delete", methods=["POST"])
@login_required
def delete():

    # Remove booking
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM events WHERE id = ?", id)
    return redirect("/bookings")


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
        id = db.execute("SELECT id FROM users WHERE email = ?", email)

        print(id)

        # # TODO Log user in *needs to be updated to index once built
        # return render_template("login.html")

    else:
        return render_template("signup.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e - InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)