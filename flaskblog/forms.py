from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import validators
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import BooleanField, EmailField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_login import current_user
from flaskblog.models import User
from flask_wtf.file import  FileField, FileAllowed
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=5, max=30)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email already exists.')
    
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
    
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired(),Email()])
    picture = FileField('Update profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is taken. Please choose a different one.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email already exists.')
    
    
class PostForm(FlaskForm):
    title  = StringField(label='Title for Post', validators=[DataRequired()])
    content = TextAreaField(label='Content for Post', validators=[DataRequired()])
    submit = SubmitField(label='POST')
    
class RequestResetForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(),Email()])
    submit = SubmitField(label='Request to password Reset')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('This email does not exists.')
            
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(),Length(min=5, max=30)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField(label='Reset password')