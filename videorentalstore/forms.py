from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, IntegerField
# from wtfroms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class CustomerForm(FlaskForm):
    first_name = StringField('Frist name',
                           validators=[DataRequired(), Length(min=1, max=50)])
    last_name = StringField('Last name',
                           validators=[DataRequired(), Length(min=1, max=50)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=1, max=120)])
    submit = SubmitField('Submit')

class RentalForm(FlaskForm):
    film_name = StringField('Film name',
                           validators=[DataRequired(), Length(min=1, max=200)])
    cust_email = StringField('Customer Email',
                        validators=[DataRequired(), Email(), Length(min=1, max=120)])
    start_date = DateField('Start date', format='%Y-%m-%d',
                        validators=[DataRequired()])
    end_date = DateField('End date', format='%Y-%m-%d', 
                        validators=[DataRequired()])
    submit = SubmitField('Submit')

class ReturnForm(FlaskForm):
    film_name = StringField('Film name',
                           validators=[DataRequired(), Length(min=1, max=200)])
    cust_email = StringField('Customer Email',
                        validators=[DataRequired(), Email(), Length(min=1, max=120)])
    start_date = DateField('Start date', format='%Y-%m-%d',
                        validators=[DataRequired()])
    due_date = DateField('Due date', format='%Y-%m-%d', 
                        validators=[DataRequired()])
    return_date = DateField('Return date', format='%Y-%m-%d', 
                        validators=[DataRequired()])
    days = IntegerField('Days',
            validators=[DataRequired()])
    late_charge = IntegerField('Late charge',
            validators=[DataRequired()])
    total_price = IntegerField('Total price (incl late charge)',
            validators=[DataRequired()])

    submit = SubmitField('Return')