from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField , SelectField , DateField
from wtforms.validators import DataRequired
from ..models import Author


class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = SelectField("Author", validators=[DataRequired()])
    publish_date = DateField('Publish Date', format='%Y-%m-%d', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    age_group = SelectField('Age Group', choices=[('Under 8', 'Under 8'),('8-15', '8-15'), ('Adult', 'Adult')], validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    def set_authors(self):
        self.author.choices = [(author.id, author.name) for author in Author.query.all()]
    
class AuthorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')