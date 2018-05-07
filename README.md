# final-project

My file and folder hierarchy follows closely with the standard Django project, i.e.,
templates are in the 'templates' folder, css files are in the 'static' folder, etc. I
made my own class called 'Cal' which is located in 'cal.py' which is in the main app
folder along with 'views.py', etc. My main and only app that I created for this
project is called 'tools'. The project's name is 'planner' hence why there's a folder
called 'planner'.

To run my program, navigate to the 'final-project' folder of my files. Then run 'pip3
install -r requirements.txt' in the terminal window. Then run 'winpty python
manage.pyrunserver' in the command line if you have Windows. Run just 'python
manage.py runserver' if that doesn't work or if you have another operating system.
Copy and paste the URL that gets displayed, to your browser.

The superuser name I created for the database is 'gerald' and the password is
"finalproject33a". I also created a username called 'stacey' and 'britney' which
both have no passwords. Feel free to add or delete usernames, data and the like for
purposes of grading.

My final project is a planner. I was hoping to create more than a calendar app for it
but the calendar app became the focal point of the project soon after I started. The
index page has the heading 'Planner' underneath of which is a link to the calendar. My
calendar app allows users to view a calendar on the screen with memos that they can
add to it by hitting the 'ADD MEMO' link on the Calendar page. Besides the date, memos
include a name and optionally a category, start and end time and description. Users
can filter memos displayed on the calendar by category. They can also add and delete
categories for their memos by hitting the 'MANAGE CATEGORIES' link on the calendar
page. The navigation just above the calendar allows users to switch to previous and
future months.

There are things I wanted to do that I didn't accomplish. One thing was that I
wanted to be able to allow users to highlight their memos on the calendar
according to category. For instance, maybe a user would want to have important
memos highlighted in red. I also wanted to implement a social calendar where
users could post events and send out invitations that other users could RSVP to.
I also would have liked to add more functionality to the calendar such as allowing
the users to delete and change more than is currently allowed and making the UI
more manageable in general. Unfortunately, I wasn't able to implement these and
other features in time.

I mostly used Google Chrome throughout the development process.
