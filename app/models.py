from werkzeug.security import generate_password_hash , check_password_hash
from typing import Annotated
from sqlalchemy.orm import Mapped , mapped_column
from flask_login import UserMixin
from . import db
from . import login_manager


class User(db.Model , UserMixin):
    Role_options = {
        'admin' : 1,
        'user' : 2
    }
    id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(unique=True)
    email : Mapped[str] = mapped_column(unique=True)
    hashed_password : Mapped[str] = mapped_column(unique=True)
    role : Mapped[int] = mapped_column(default=Role_options['user'])


    def set_role(self, role):
        if role in self.Role_options:
            self.role = self.Role_options[role]
        else:
            raise ValueError(f"Invalid role: {role}")

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def is_admin(self):
        return self.role == self.Role_options['admin']


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', back_populates='author')


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    publish_date = db.Column(db.String(10), nullable=False)
    added = db.Column(db.DateTime, default=db.func.now())
    price = db.Column(db.Integer, nullable=False)
    age_group = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author', back_populates='books')

