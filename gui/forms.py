
from wtforms import Form
from wtforms import StringField, EmailField, PasswordField, SelectMultipleField
from wtforms.validators import InputRequired, Length, Email
from lib import PERM_ADMIN, PERM_POWER, PERM_VIEW_PACKETS, PERM_VIEW_LOGS, PERM_EXPORT_PACKETS, PERM_EXPORT_LOGS, PERM_REGISTER, PERM_LOGIN, PERM_EDIT_OWN, PERM_EDIT_OTHER, PERM_DELETE_OWN, PERM_DELETE_OTHER

PERMS = (
    (PERM_ADMIN, PERM_ADMIN),
    (PERM_POWER, PERM_POWER),
    (PERM_VIEW_LOGS, PERM_VIEW_LOGS),
    (PERM_VIEW_PACKETS, PERM_VIEW_PACKETS),
    (PERM_EXPORT_LOGS, PERM_EXPORT_LOGS),
    (PERM_EXPORT_PACKETS, PERM_EXPORT_PACKETS),
    (PERM_REGISTER, PERM_REGISTER),
    (PERM_LOGIN, PERM_LOGIN),
    (PERM_EDIT_OWN, PERM_EDIT_OWN),
    (PERM_EDIT_OTHER, PERM_EDIT_OTHER),
    (PERM_DELETE_OWN, PERM_DELETE_OWN),
    (PERM_DELETE_OTHER, PERM_DELETE_OTHER)
)

class LoginForm(Form):
    username = StringField('Username:', validators=[InputRequired(), Length(min=5, max=16)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=5, max=64)])

class RegisterForm(LoginForm):
    email = EmailField('Email:', validators=[Email()])
    perms = SelectMultipleField('Permissions:', choices=PERMS)