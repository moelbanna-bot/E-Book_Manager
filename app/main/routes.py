from flask import Blueprint
from flask_login import login_required
from flask import render_template, redirect, url_for
from ..models import Book, Author
from .forms import BookForm, AuthorForm
from app import db

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
@login_required
def index():
    books = Book.query.all()
    return render_template('book_store/books.html' , books = books)


@main_blueprint.route('/author' , methods=['GET' , 'POST'])
@login_required
def add_author():
    form = AuthorForm()
    if form.validate_on_submit():
        author = Author(name=form.name.data)
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('main.add_book'))
    return render_template('book_store/author_form.html' , form=form)

@main_blueprint.route('/book' , methods=['GET' , 'POST'])
@login_required
def add_book():
    form = BookForm()
    form.set_authors()
    if form.validate_on_submit():
        author = Author.query.filter_by(id=form.author.data).first()
        book = Book(title=form.title.data , publish_date=form.publish_date.data , price=form.price.data , age_group=form.age_group.data , author=author)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('book_store/book_form.html' , form=form)

@main_blueprint.route('/books/<int:book_id>')
@login_required
def book_details(book_id):
    book = Book.query.get(book_id)
    return render_template('book_store/book_details.html' , book=book)

@main_blueprint.route('/author/<int:author_id>')
@login_required
def author_details(author_id):
    author = Author.query.get(author_id)
    author_books = author.books
    return render_template('book_store/author_details.html' , author=author , author_books=author_books)

@main_blueprint.route('/delete_book/<int:book_id>')
@login_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('main.index'))