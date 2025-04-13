from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, CourseInfo
import openai
import OPENAI_API_KEY
import os

def generateContribution():
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