from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
# from wtfroms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class CustomerForm(FlaskForm):
    first_name = StringField('Frist name',
                           validators=[DataRequired(), Length(min=1, max=50)])
    last_name = StringField('Last name',
                           validators=[DataRequired(), Length(min=1, max=50)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=1, max=120)])
    submit = SubmitField('Add')

class RentalForm(FlaskForm):
    film_name = StringField('Film name',
                           validators=[DataRequired(), Length(min=1, max=200)])
    cust_email = StringField('Customer Email',
                        validators=[DataRequired(), Email(), Length(min=1, max=120)])
    start_date = DateField('Start date', format='%Y-%m-%d',
                        validators=[DataRequired()])
    end_date = DateField('End date', format='%Y-%m-%d', 
                        validators=[DataRequired()])
    submit = SubmitField('Add')