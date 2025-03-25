from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    comments = db.relationship('Comment', backref='thread', cascade="all, delete-orphan", lazy=True)

    def __repr__(self) -> str:
        string = f"ID: {self.id}, Title: {self.title}, Content: {self.content}, Created_At: {self.created_at}, Comments: {self.comments}"
        return string
    
    def serialize(self):
        return {"id": self.id,\
                "title": self.title,\
                "content": self.content}

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())