from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Lead(db.Model):
    """Model for storing lead information from contact form"""
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)
    project_details = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='new')  # new, contacted, qualified, converted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)
    budget = db.Column(db.String(100), nullable=True)
    timeline = db.Column(db.String(100), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'company': self.company,
            'email': self.email,
            'phone': self.phone,
            'project_details': self.project_details,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'notes': self.notes,
            'budget': self.budget,
            'timeline': self.timeline
        }
    
    def __repr__(self):
        return f'<Lead {self.name} - {self.email}>'


class PortfolioItem(db.Model):
    """Model for portfolio items (projects)"""
    __tablename__ = 'portfolio'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_filename = db.Column(db.String(300), nullable=True)
    visible = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_filename': self.image_filename,
            'visible': self.visible,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Testimonial(db.Model):
    """Model for testimonials"""
    __tablename__ = 'testimonials'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200), nullable=True)
    message = db.Column(db.Text, nullable=True)
    image_filename = db.Column(db.String(300), nullable=True)
    visible = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'message': self.message,
            'image_filename': self.image_filename,
            'visible': self.visible,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
