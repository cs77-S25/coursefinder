from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, CourseInfo
#import openai
#import OPENAI_API_KEY
import os

app = Flask(__name__)

# Read API key from file and export it to environment
with open('api_key.txt', 'r') as file:
    openai_apikey = file.read().strip()
os.environ['OPENAI_API_KEY'] = openai_apikey

# Set OpenAI API key for use
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure database
app.config['CACHE_TYPE'] = 'null' # disable if in production environment
app.config['SECRET_KEY'] = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS
CORS(app)

# Initialize db to be used with current Flask app
with app.app_context():
    db.init_app(app)

    # Create the database if it doesn't exist
    # Note: create_all does NOT update tables if they are already in the database. 
    # If you change a model’s columns, use a migration library like Alembic with Flask-Alembic 
    # or Flask-Migrate to generate migrations that update the database schema.
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html', active="home")

import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import openai

# === API KEY SETUP ===
# Read API key from file and export it to environment
with open('api_key.txt', 'r') as file:
    openai_apikey = file.read().strip()
os.environ['OPENAI_API_KEY'] = openai_apikey

# Set OpenAI API key for use
openai.api_key = os.getenv("OPENAI_API_KEY")

# === FLASK SETUP ===
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coursefinder.db'
db = SQLAlchemy(app)

# === DATABASE MODEL ===
from sqlalchemy.dialects.postgresql import ARRAY  # If using Postgres; for SQLite, use PickleType or JSON
from sqlalchemy.types import Float

class CourseFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    professor = db.Column(db.String(100))
    embedding = db.Column(ARRAY(Float), nullable=False)  # Adjust if not using PostgreSQL

# === ROUTE FOR CONTRIBUTE PAGE ===
@app.route('/contribute', methods=['GET', 'POST'])
def contribute():
    if request.method == 'POST':
        # Collect form inputs
        course_name = request.form.get('course_name')
        professor = request.form.get('professor')
        embedding_text = request.form.get('embedding_text')  # Hidden field populated by JS

        # Generate embedding from OpenAI
        response = openai.Embedding.create(
            input=embedding_text,
            model="text-embedding-ada-002"
        )
        embedding_vector = response['data'][0]['embedding']

        # Save to DB
        new_feedback = CourseFeedback(
            course_name=course_name,
            professor=professor,
            embedding=embedding_vector
        )
        db.session.add(new_feedback)
        db.session.commit()

        return redirect(url_for('contribute'))

    return render_template('contribute.html')


#@app.route('/contribute')
#def contribute():
#    return render_template('contribute.html', active="contribute")

@app.route('/quiz')
def quiz():
    return render_template('quiz.html', active="quiz")

@app.route('/login')
def login():
    return render_template('login.html', active="login")

# @app.route('/thread/<int:thread_id>')
# def thread(thread_id):
#     thread = Thread.query.get_or_404(thread_id) # returns a 404 error if get fails
#     print(thread)
#     return render_template('thread.html', thread=thread) # return the thread object

# @app.route('/new_thread', methods=['POST'])
# def new_thread():
#     form = request.get_json()
#     title = form["title"]
#     content = form["content"]
#     if title and content:
#         new_thread = Thread(title=title, content=content)
#         db.session.add(new_thread)
#         db.session.commit()
#         print(f"Added new thread: {new_thread.serialize()}")
#         return make_response(jsonify({"success": "true", "thread": new_thread.serialize()}), 200) # return both JSON object and HTTP response status (200: OK)

#     return make_response(jsonify({"success": "false"}), 400) # return both JSON object and HTTP response status (400: bad request)

# @app.route('/comment/<int:thread_id>', methods=['POST'])
# def comment(thread_id):
#     thread = Thread.query.get_or_404(thread_id) # returns a 404 error if get fails
#     comment_text = request.form.get('comment')
#     if comment_text:
#         new_comment = Comment(thread_id=thread.id, content=comment_text)
#         db.session.add(new_comment)
#         db.session.commit()

#     return redirect(url_for('thread', thread_id=thread_id)) # set variable thread_id to be thread_id

if __name__ == '__main__':
    app.run(debug=True)
