from flask_wtf import FlaskForm
from wtforms_alchemy import ModelForm

#from flask_babel import gettext
from wtforms import StringField, BooleanField, TextAreaField, PasswordField, SelectField, DateField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from .models import User, Mobility

'''
from wtforms_alchemy import model_form_factory
BaseModelForm=model_form_factory(FlaskForm)
class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session
'''


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class ManpowerForm(ModelForm):
    class Meta:
        model=User
        unique_validator=None
        exclude=['password_hash', 'last_seen', 'username']


class MobilityForm(ModelForm):
    class Meta:
        model=Mobility
    '''
    def validate(self):
        if not Form.validate(self):
            return False
        if self.username.data == self.original_username:
            return True
        if self.username.data != User.make_valid_username(self.username.data):
            self.username.errors.append(gettext(
            'This username has invalid characters. '
            'Please use letters, numbers, dots and underscores only.'))
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None:
            self.username.errors.append(gettext(
                'This username is already in use. '
                'Please choose another one.'))
            return False
        return True
    '''


class RegistrationForm(FlaskForm):
    username=StringField('Username', validators=[Length(min=4, max=25)])
    email=StringField('Email')
    password = PasswordField('Password', validators=[DataRequired(),
        EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    remember_me = BooleanField('remember_me', default=False)


class EditForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
    password = PasswordField('New Password', validators=[EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat New Password')

    def __init__(self, original_username, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.original_username = original_username

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.username.data == self.original_username:
            return True
        if self.username.data != User.make_valid_username(self.username.data):
            self.username.errors.append(gettext(
            'This username has invalid characters. '
            'Please use letters, numbers, dots and underscores only.'))
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None:
            self.username.errors.append(gettext(
                'This username is already in use. '
                'Please choose another one.'))
            return False
        return True


class PostForm(FlaskForm):
    post = StringField('post', validators=[DataRequired()])


class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])