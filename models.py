from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from sqlalchemy import Integer, String, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
import numpy as np


db = SQLAlchemy()

# Association table for matched courses (Many-to-Many)
# A single course can be matched to many users
# Many users can be matched to a single course
# Use the id of the student or the id of the course to define relationship
matched_courses = db.Table('matched_courses',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course_info.id'))
)

class CourseReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course_info.id'), nullable=False)
    embedding = db.Column(db.Text)  # JSON string of user's review embedding
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def set_embedding(self, vector):
        self.embedding = json.dumps(vector)

    def get_embedding(self):
        return json.loads(self.embedding)

class CourseInfo(db.Model):
    __tablename__ = 'course_info'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(120), nullable=False)
    professor = db.Column(db.String(120), nullable=False)
    embedding = db.Column(db.Text, nullable=False) # stored as JSON string
    submission_count = db.Column(db.Integer, default=1) # for averaging submission vectors

    def set_embedding(self, vector):
        self.embedding = json.dumps(vector)

    def get_embedding(self):
        return np.array(json.loads(self.embedding))  # Converts the JSON string back to a numpy array
    
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now)

    # One-to-Many: Reviews the user submitted
    reviews = db.relationship('CourseReview', backref='student', lazy=True)

    # Many-to-Many: Courses matched via quiz
    matched = db.relationship('CourseInfo',
                              secondary=matched_courses,
                              backref=db.backref('matched_by_users', lazy='dynamic'))



