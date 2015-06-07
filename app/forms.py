from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField,  SubmitField, TextAreaField
from wtforms.validators import Required, Email
from models import User

class LoginForm(Form):
    openid= TextField('openid', validators=[Required()])
    remember_me=BooleanField('remember_me', default=False)
    
class SignupForm(Form):
    nickname=TextField('Nickname', validators=[Required()])
    email = TextField("Email",  [Required("Please enter your email address."), Email("Please enter your email address.")])
    password = PasswordField('Password', [Required("Please enter a password.")])
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

class SigninForm(Form):
    email = TextField("Email",  [Required("Please enter your email address."), Email("Please enter your email address.")])
    password = PasswordField('Password', [Required("Please enter a password.")])
    submit = SubmitField("Sign In")
   
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
 
    def validate(self):
        if not Form.validate(self):
            return False
     
        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.email.errors.append("Invalid e-mail or password")
            return False

class PostForm(Form):
    post = TextAreaField('post', validators = [Required()])

class AnswerForm(Form):
    answer = TextAreaField('post', validators = [Required()])

