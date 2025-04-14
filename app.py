from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, CourseReview, CourseInfo, Student
from openai import OpenAI
import os
from flask import session, flash
from werkzeug.security import check_password_hash

app = Flask(__name__)

# Configure database
app.config['CACHE_TYPE'] = 'null' # disable if in production environment
app.config['SECRET_KEY'] = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Read API key from file and export it to environment
with open('api_key.txt', 'r') as file:
    openai_apikey = file.read().strip()
os.environ['OPENAI_API_KEY'] = openai_apikey

#have the client pick up the OpenAI environmental variable
client = OpenAI()

# Enable CORS
CORS(app)

# Initialize db to be used with current Flask app
with app.app_context():
    db.init_app(app)

    # Create the database if it doesn't exist
    # Note: create_all does NOT update tables if they are already in the database. 
    # If you change a model’s columns, use a migration library like Alembic with Flask-Alembic 
    # or Flask-Migrate to generate migrations that update the database schema.


    #have the wiping of the database built in for development: 
    db.drop_all()

    db.create_all()

@app.route('/')
def home():
    return render_template('home.html', active="home")

# Multipurpose route for the contribute page 
@app.route('/contribute', methods=['GET', 'POST'])
def contribute():
    # Check if user is logged in
    if 'user_email' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    if request.method == 'POST':
        # Get form fields
        course_name = request.form.get('course_name')
        professor = request.form.get('professor')
        department = request.form.get('department')
        embedding_text = request.form.get('embedding_text')  # From hidden field via JS

        # Generate embedding
        response = client.embeddings.create( 
            input=embedding_text, 
            model="text-embedding-ada-002" 
        ) 
        embedding_vector = response.data[0].embedding

        # Save to DB using JSON format
        new_feedback = CourseInfo(
            course_name=course_name,
            department=department,
            professor=professor
        )
        new_feedback.set_embedding(embedding_vector)

        # Add CourseInfo feedback to the session first
        db.session.add(new_feedback)
        db.session.flush()  # This assigns an ID to new_feedback without committing

        # Create a new review and associate it with the logged-in user
        new_review = CourseReview(
            student_id=session['user_id'],  # Use the user_id from session
            course_id=new_feedback.id
        )
        new_review.set_embedding(embedding_vector)

        # Add review to session and commit to the database
        db.session.add(new_review)
        db.session.commit()

        return redirect(url_for('home'))  # Redirect to home after submission

    return render_template('contribute.html', active="contribute")

@app.route('/quiz')
def quiz():
    return render_template('quiz.html', active="quiz")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input = request.form.get('login')  # Get user input from form

        # Check if the input is an email (new user)
        if '@' in user_input:
            # It's an email address, so creating a new user
            user_email = user_input
            # Check if email already exists
            existing_user = Student.query.filter_by(email=user_email).first()
            if existing_user:
                # User exists, login them directly
                session['user_email'] = existing_user.email
                session['user_id'] = existing_user.id
                return redirect(url_for('home'))  # Redirect to home or a dashboard

            else:
                # Create a new user; first grab username for db init from email 
                new_user = Student(username=user_email.split('@')[0], email=user_email) 
                db.session.add(new_user)
                db.session.commit()
                session['user_email'] = new_user.email
                session['user_id'] = new_user.id
                return redirect(url_for('home'))  # Redirect to home or a dashboard

        else:
            # It's a username, so we're logging in a returning user
            username = user_input
            existing_user = Student.query.filter_by(username=username).first()

            if existing_user:
                # User exists, login them directly
                session['user_email'] = existing_user.email
                session['user_id'] = existing_user.id
                return redirect(url_for('home'))  # Redirect to home or a dashboard
            else:
                # User not found, show an error or prompt to sign up
                flash("User not found. Please sign up.", "danger")
                return render_template('login.html', active="login")

    return render_template('login.html', active="login")
if __name__ == '__main__':
    app.run(debug=True)
