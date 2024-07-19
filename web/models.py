from .main import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    user=db.Column(db.String(120),unique=True)
    password=db.Column(db.String(120))
    firstName=db.Column(db.String(50))
    blogs=db.relationship('Blog',backref='user',passive_deletes=True)
    comments=db.relationship('Comment',backref='user',passive_deletes=True)
    def __repr__(self):
        return self.user
    


class Blog(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    blog=db.Column(db.Text(),nullable=False)
    date=db.Column(db.DateTime(timezone=True),default=func.now())
    author=db.Column(db.String(120),db.ForeignKey('user.user',ondelete='CASCADE'),nullable=False)
    comments=db.relationship('Comment',backref='blog',passive_deletes=True)
class Comment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    comment=db.Column(db.String(200),nullable=False)
    date=db.Column(db.DateTime(timezone=True),default=func.now())
    author=db.Column(db.String(120),db.ForeignKey('user.user',ondelete='CASCADE'),nullable=False)
    blog_id=db.Column(db.Integer,db.ForeignKey('blog.id',ondelete='CASCADE'),nullable=False)
    
