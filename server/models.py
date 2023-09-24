from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    _password_hash = db.Column(db.String)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    # [x] incorporate bcrypt to create a secure password. Attempts to access the password_hash should be met with an AttributeError.
    # [x] validate the user's username to ensure that it is present and unique (no two users can have the same username).
    # [x] have many recipes.

    @hybrid_property
    def password_hash(self):
        raise Exception('Password hashes may not be viewed.')
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))

    def __repr__(self):
        return f'User {self.username}, ID: {self.id}'



# Add validations for the Recipe model:

# [x] Title must be present.
# [] Instructions must be present and at least 50 characters long.]
class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    # A recipe belongs to a user. 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String)
    minutes_to_complete = db.Column(db.String)

    users = db.relationship('User', backref='recipes')

    @validates('instructions')
    def validate_instructions_length(self, key, value):
        if len(value) < 50:
            raise ValueError("instructions must be at least 50characters in length.")
        return value




    pass