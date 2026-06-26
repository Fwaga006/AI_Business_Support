from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    information = db.Column(db.Text)

    def __repr__(self):
        return self.business_name
class ChatMessage(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    business_id = db.Column(db.Integer, db.ForeignKey("business.id"))

    customer_message = db.Column(db.Text)

    ai_response = db.Column(db.Text)
created_at = db.Column(db.DateTime, default=db.func.now())