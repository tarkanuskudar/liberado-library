from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, RadioField, DateField, HiddenField
from wtforms.validators import ValidationError
import tools as tls


# wtforms library


# we create an instance in our app
class RegisterForm(FlaskForm):
    def length_check(self, field):
        if len(field.data) < 8:
            raise ValidationError(f'Your {field.name} must be at least 8 characters long')

    username = StringField("Username")
    email = EmailField("Email")
    password = PasswordField("Password ", [length_check])
    submit = SubmitField("Submit")
    gender = RadioField("Gender", choices=[("male", "Male"), ("female", "Female"), ("non-binary", "Non-binary"),
                                           ("not_to_say", "Prefer not to say")])
    birth_date = DateField("Birthdate", format='%Y-%m-%d')
    street = StringField("Street Number and Name")
    postcode = StringField("Postcode")
    city = StringField("City")
    matriculation = StringField("Matriculation Number")
    name = StringField("Name")

    # check if the username already exists in our CSV
    def validate_username(self, field):
        if tls.check_register(field.data):
            raise ValidationError(f"Username {field.data} already exists!")

    def validate_email(self, field):
        if tls.check_register(field.data):
            raise ValidationError(f"Email {field.data} already exists!")

    def validate_matriculation(self, field):
        if tls.check_register(field.data):
            raise ValidationError(f"Matriculation number {field.data} already exists!")


class Loginform(FlaskForm):
    username = StringField("Username: ")
    password = PasswordField("Password: ")
    submit = SubmitField("Submit")

    valUsername = ""

    # check if the username already exists in our CSV
    def validate_username(self, field):
        self.valUsername = field.data
        if not tls.check_login_username(field.data):
            raise ValidationError(f'The username or password is incorrect')  # error message

    def validate_password(self, field):
        if not tls.check_login_password(self.valUsername, field.data):
            raise ValidationError(f'The username or password is incorrect')  # error message
