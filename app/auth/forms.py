from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email

class LoginForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(),Length(1,60)])
    password = PasswordField('密码',validators=[DataRequired()])
    submit = SubmitField('登录')
