from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
import json

db = SQLAlchemy()

class CourseInfo(db.Model):
    __tablename__ = 'course_info'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(120), nullable=False)
    professor = db.Column(db.String(120), nullable=False)
    embedding = db.Column(db.Text, nullable=False)  # stored as JSON string

    def set_embedding(self, vector):
        self.embedding = json.dumps(vector)

    def get_embedding(self):
        return json.loads(self.embedding)

    
    def __repr__(self) -> str:
        string = f"ID: {self.id}, Title: {self.title}, Content: {self.content}, Created_At: {self.created_at}, Comments: {self.comments}"
        return string
    
    def serialize(self):
        return {"id": self.id,\
                "title": self.title,\
                "content": self.content}

#class Comment(db.Model):
#id = db.Column(db.Integer, primary_key=True)
#thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
#content = db.Column(db.Text, nullable=False)
#created_at = db.Column(db.DateTime, default=db.func.current_timestamp())