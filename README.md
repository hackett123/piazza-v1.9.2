# piazza-v1.9.2

## About

This is a modern and reimagined creation of Piazza, a Q&A forum for university courses, designed and implemented by Jamie Tomlinson and Michael Hackett via the Django web dev framework, Bulma CSS frameworks, JQuery, and 2Select libraries. Additional CSS provided courtesty of Bulma Swatch. All other content and all design choices are our own.

## Installation Instructions

Refer below for the necessary packages you will need to pip install in order to run the project (as we have not deployed with Heroku or Docker). We recommend virtualenv so as to isolate this project and avoid potential conflicts with other packages or python2.


## Dependencies

(Also available under requirements.txt)

autopep8==1.4.4
Django==2.2
pycodestyle==2.5.0
pytz==2019.1
sqlparse==0.3.0


## APIs

### First Party APIs

Imported time and csv so as to allow for instructors to export csv files of course content.

### Third Party APIs

Django is the largest framework we've integrated into the assignment, but there is also a great deal of javascript built into the background, particularly through the use of JQuery and 2Select.

## Design Decisions

We built Piazza v1.9.2 in order to facilitate the process of creating and maintaining a field of communication between students and instructors. As such, we placed serious consideration and concern into the SQL backend we built as well as the front-end development. These choices reflect what we believe are best practices for development and simplest interactions for users.

## Routes

### Splash

Splash route acts as the home page which provides login and signup links.

### Login

Standard login to view a user's homepage, authenticates user credentials with SQL backend.

### Logout

Standard logout.

### Signup

Sign up procedure to become a user for Piazza v1.9.2

### Create Course

Become instructor of a new course on Piazza v1.9.2 by providing course name, code, term, and select all initial students and TAs.

### Course

Home page for a specific course. Shows all posts, folders, and options to create new posts or notes and see all posts in further detail.

### Create Post

Create a post or note to everybody or just to instructors.

### Render Post Form

This redirects to the course home page after making a post.

### Delete Course

This is a feature only available to instructors which will remove the course from Piazza v1.9.2

### Join Course

Students can enroll in courses that they are not yet enrolled in.

### View Post

While on a course's home page, you can expand a post to see it in more detail, as well as answers from students / instructors and followups.

### Add Followup

Students and instructors can add followups to posts.

### Add Instructor Answer

Instructors and TAs can answer questions.

### Add Student Answer

Students can answer questions.

### Folder

Can filter all posts based off of a specific folder from a course home page.

### Manage

An instructor has sole access to this page. Functionality includes adding and removing students and TAs from the course, as well as course statistics on who is enrolled in the course or a TA in the course. This also allows sole access to the ability to delete courses.

### Update Course

Any edits made by the instructor in manage are sent to this route to update the database.

### Edit Followup

The author of a followup can edit the contents of the followup.

### Edit Post

The author of a post can edit the contents of the post.

### Edit Instructor Answer

The author of an instructor answer can edit the contents of the response.

### Edit Student Answer

The author of a student answer can edit the contents of the response.

### Export Course

The instructor can export a csv file of course contents, including all student and TA information and all post contents.