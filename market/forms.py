from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField, SubmitField
from wtforms.validators import Length , EqualTo , Email , DataRequired , ValidationError
from market.Models import User

class RegisterForm(FlaskForm):
    def validate_username(self,username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("User name Already exists")
    def validate_email_add(self, email_add_to_check):
        email = User.query.filter_by(email_add = email_add_to_check.data).first()
        if email :
            raise ValidationError("Email is used")
    username = StringField(label='User Name' , validators=[Length(min = 2 , max= 20) , DataRequired()]) 
    email_add = StringField(label='E-mail' , validators=[Email() , DataRequired()])
    password1 = PasswordField(label= 'Password' , validators=[Length(min = 8 ) , DataRequired()])
    password2 = PasswordField(label= 'Confirm Password' , validators=[EqualTo('password1') , DataRequired()])
    submit = SubmitField(label = 'Create Account')  


class LoginForm(FlaskForm):
    username = StringField(label='User Name' , validators= [DataRequired()]) 
    password = PasswordField(label= 'Password' , validators= [DataRequired()])
    submit = SubmitField(label = 'Sign In') 

class PurchaseForm(FlaskForm):
    submit = SubmitField(label = 'Purchase Item')

class SellForm(FlaskForm):
    submit = SubmitField(label = 'Sell Item')