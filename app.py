from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, CourseReview, CourseInfo, Student
from openai import OpenAI
import os
from flask import session, flash
from werkzeug.security import check_password_hash
from utils import get_best_course_match
import numpy as np
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure database
app.config['CACHE_TYPE'] = 'null' # disable if in production environment
app.config['SECRET_KEY'] = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Read API key from local file and export it to environment
#with open('api_key.txt', 'r') as file:
#    openai_apikey = file.read().strip()
#os.environ['OPENAI_API_KEY'] = openai_apikey
#os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

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
    

    db.create_all()

@app.route('/')
def home():
    return render_template('home.html', active="home")

# Multipurpose route for the contribute page 
@app.route('/contribute', methods=['GET', 'POST'])
def contribute():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Get form fields
        course_name = request.form.get('course_name')
        professor = request.form.get('professor')
        department = request.form.get('department')
        embedding_text = request.form.get('embedding_text')

        # Generate embedding
        response = client.embeddings.create( 
            input=embedding_text, 
            model="text-embedding-ada-002" 
        )
        embedding_vector = np.array(response.data[0].embedding)  # Use numpy array for math

        # Check if course already exists
        existing_course = CourseInfo.query.filter_by(course_name=course_name, \
        department=department, professor=professor).first()

        if existing_course:
            # Update existing course embedding by averaging
            old_embedding = existing_course.get_embedding()
            old_count = existing_course.submission_count

            new_average = (old_embedding * old_count + embedding_vector) / (old_count + 1)

            existing_course.set_embedding(new_average.tolist())  # save as JSON serializable list
            existing_course.submission_count += 1 #increment number of reviews for existing course

            db.session.add(existing_course)
            db.session.flush()
            print("Modified existing course")

            course_id = existing_course.id
        else:
            # Create new course if it doesn't exist
            new_course = CourseInfo(
                course_name=course_name,
                department=department,
                professor=professor
            )
            new_course.set_embedding(embedding_vector.tolist())
            db.session.add(new_course)
            db.session.flush()

            course_id = new_course.id

        # Create a new review and associate it with the user
        new_review = CourseReview(
            student_id=session['user_id'],
            course_id=course_id
        )
        new_review.set_embedding(embedding_vector.tolist())

        db.session.add(new_review)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('contribute.html', active="contribute")


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        department_preference = request.form.get('department')

        # Build embedding text based on quiz form input
        embedding_text = request.form.get("personality_embedding")
        if not embedding_text:
            raise ValueError("Missing input for embedding!")

        response = client.embeddings.create(
            input=embedding_text,
            model="text-embedding-ada-002"
        )
        quiz_vector = response.data[0].embedding

        course_options = db.session.query(CourseInfo).filter_by(department=department_preference).all()
        best_course = get_best_course_match(quiz_vector, course_options)

        if best_course:
            student = Student.query.get(session['user_id'])
            if best_course not in student.matched:
                student.matched.append(best_course)
                db.session.commit()

            # Redirect while passing course_id of best_course db field
            return redirect(url_for('success', course_id=best_course.id))
        else:
            flash("No matching courses found in this department.", "warning")
            return redirect(url_for('quiz'))

    return render_template('quiz.html', active="quiz")


@app.route('/success/<int:course_id>')
def success(course_id):
    course = CourseInfo.query.get(course_id)
    if course:
        return render_template('success.html', active="success", match=course, professor=course.professor)

    else:
        flash("Course not found.", "error")
        return redirect(url_for('quiz'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get user input from the form
        signup_email = request.form.get('signup_email')  # For sign up
        login_id = request.form.get('login_id')  # For login

        # Handle sign-up case (email input)
        if signup_email:
            user_email = signup_email
            # Check if email already exists
            existing_user = Student.query.filter_by(email=user_email).first()
            if existing_user:
                # User exists, log them in directly
                session['user_email'] = existing_user.email
                session['user_id'] = existing_user.id
                return redirect(url_for('home'))  # Redirect to home or a dashboard
            else:
                # Create a new user
                new_user = Student(username=user_email.split('@')[0], email=user_email)
                db.session.add(new_user) #add newly created user to session
                db.session.commit()
                session['user_email'] = new_user.email #update email and user id
                session['user_id'] = new_user.id
                return redirect(url_for('home'))  # Redirect to home or a dashboard
        
        # Handle login case (username input/returning user)
        elif login_id:
            username = login_id
            existing_user = Student.query.filter_by(username=username).first()

            if existing_user:
                # User exists, log them in directly
                session['user_email'] = existing_user.email
                session['user_id'] = existing_user.id
                return redirect(url_for('home'))  # Redirect to home or a dashboard
            else:
                # User not found, show an error or prompt to sign up
                flash("User not found. Please sign up.", "danger")
                return render_template('login.html', active="login")

        # If no input is provided
        flash("Please enter a valid email or username to continue.", "danger")
        return render_template('login.html', active="login")

    return render_template('login.html', active="login")



if __name__ == '__main__':
    app.run(debug=True)
