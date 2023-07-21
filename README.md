# Nightingale Bowden booking system
#### Video Demo:  <URL HERE>
#### Description:
The Nightingale Bowden booking system is my final project for CS50X. I live in a new apartment building which has a communal rooftop garden and barbeque area available for all residents. Up until now, we have used an adhoc method of reserving the space by posting on our Slack channel. Someone might post 'Hey folks, I'm having some friends round on Saturday night and planning to head up to the roof after dinner. I hope this doesn't clash with anyone else's plans?'. There is no way to view if someone is planning to use the roof on a particular date without trawling through the channel for messages, so it's not a very good system. This web application is designed to solve this problem, by creating a booking system for residents. Residents can create an account and log in to view existing bookings, make a booking, and edit or delete their own upcoming bookings. Additionally, admin functionality is provided to enable specific users (e.g. the management committee) to view, edit or delete bookings made by all users.

The web application is built using HTML, CSS and Bootstrap 5 in the front end, Python and Flask in the back end, and a SQLite database.

The database, ngbowden.db, contains two tables: users and events. The users table records details of each user who creates an account, containing an auto-generated unique id number, their firstname, email, apartment number, password hash and whether or not they have admin access. The events table contains an auto-generated event id, event name, date, start and end date, and links to the users table via user id.

There are two Python files: app.py and helpers.py. app.py is the main Python file containing all the routes for the application. helpers.py contains helper functions used within app.py.

The templates folder contains all of the HTML templates for the application. The static folder contains the CSS and JavaScript files along with images.

The layout.html file is the master file which all other templates extend via Jinja.

navigation.html contains the navigation bar and is added to each of the other pages, excluding the signup and login pages. This enables any changes to the navbar to be made once only, and applied site-wide.

login.html displays the login page, with a link for new users to signup.

signup.html is where a new user can create an account.

index.html is the homepage, which includes a short introduction to the portal, an image of the rooftop space and a list of the users' upcoming bookings. From here, a user can make a new booking or edit/delete an existing booking. I considered including two sections on this page - upcoming bookings and past bookings, but ultimately I decided to keep it simple and display upcoming bookings only, as users are unlikely to want to view old bookings. This feature could be added in the future if the need was identified.

book.html is the page the user visits to make a new booking. One of the primary features of this web application is a calendar which loads on the booking page to display all existing bookings. This is built entirely using JavaScript, and the code is contained in 'calendar.js'. When the page loads, the current month is displayed on the calendar, and a fetch request gets details of any existing events for this month and adds them to the relevant day. The user can then click arrow buttons to navigate forward and backward through the calendar, which updates dynamically without the page reloading. Once the user finds the date and time they would like to book and checks that it is free, they can use the form on the same page to submit details of their event. 

Client side form validation is in place on each of the required fields as well as server side validation to ensure the booking is valid. A booking will be rejected if it clashes with an existing booking, if form fields are incomplete, or if the booking is in the past. If a booking is successful, it is added to the database.

To enhance user experience on this page, I decided to implement modals which display a relevant error message if a booking is unsuccessful, or a confirmation message if the booking is successful. Elsewhere on the site, if an error is encountered, the user is directed to apology.html. In this case, I don't want to direct a user to a different page if their booking fails, so I decided modals here would be a better design option.

Once a user has a booking, they can edit or delete it from the home page (also accessible via the 'Manage my bookings' link in the navigation menu).
A two-step delete is implemented, so when the delete button is clicked a modal pops up asking user to confirm deletion. Upon confirmation, the event is removed from the database.

For the edit functionality, I was originally intending to implement via a modal pop up. However, I eventually decided that it would be better to display the calendar for the user so they can check the alternative date/time they may want to select is available. This is achieved by rendering edit.html. Edit.html is very similar to book.html however the form fields are populated with the details of the existing booking at first, and can then be edited by the user. This helps the user to know which event they are editing. When a user confirms the changes to their booking, validation occurs to ensure the booking is valid and if successful, the database entry for this specific event is updated with the new data.

The calendar.js file is only relevant for use when making a booking or editing an existing booking and is therefore linked in the book.html and edit.html files.

Finally, account.html displays details of the currently logged in user. In the future, this could include the option to update password or change personal details.

When I decided on this as my final project, I felt overwhelmed by what I would need to do, and wasn't sure how I would implement it, or if it was even possible with my beginner knowledge of the technologies I was planning to use. Building this full stack application challenged me greatly, provided me with plenty of frustrating moments but ultimately, showed me that I could go from zero to a fully functioning modern web-application with enough time and persistence. I have so much more to learn, but I am very proud of what I've created. Thank you CS50 team!
