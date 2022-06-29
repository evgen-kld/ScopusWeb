from app  import db
import sqlalchemy as sa

class Author(db.Model):
    __tablename__ = 'authors'
    author_id = db.Column(db.String(15), primary_key=True)
    document_count = db.Column(db.Integer)
    affiliation_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Author: %r>' % self.author_id

class Author_Fullname(db.Model):
    __tablename__ = 'authors_fullname' 
    id = db.Column(db.Integer, primary_key=True)   
    author_id = db.Column(db.String(15), db.ForeignKey('authors.author_id'))
    surname = db.Column(db.String(30))
    given_name = db.Column(db.String(30))
    initials = db.Column(db.String(30))
    is_preferred = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Author Fullname: {self.surname} {self.initials}>'    










