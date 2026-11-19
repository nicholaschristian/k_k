from datetime import date

from flask_wtf import FlaskForm
from wtforms import (
    DateField, EmailField, IntegerField, PasswordField, SelectField, StringField, TextAreaField,
)
from wtforms.validators import (
    DataRequired, Email, InputRequired, Length, NumberRange, Optional, ValidationError,
)

from app.content import EVENT_TYPES, PACKAGE_CHOICES


class InquiryForm(FlaskForm):
    name = StringField("Your name", validators=[DataRequired("Enter your name."), Length(max=120)])
    email = EmailField(
        "Email",
        validators=[
            DataRequired("Enter an email so we can reply."),
            Email("Enter a valid email address, like you@example.com.", check_deliverability=False),
            Length(max=200),
        ],
    )
    phone = StringField("Phone", validators=[Optional(), Length(max=40)])
    event_date = DateField(
        "Event date", validators=[InputRequired("Choose the date of your event.")]
    )
    event_type = SelectField(
        "Type of event",
        choices=[("", "Choose one")] + EVENT_TYPES,
        validators=[DataRequired("Choose the type of event.")],
    )
    guest_count = IntegerField(
        "Guest count",
        validators=[
            InputRequired("Enter a rough guest count."),
            NumberRange(min=1, max=5000, message="Enter a guest count between 1 and 5,000."),
        ],
    )
    location = StringField(
        "Venue or city",
        validators=[DataRequired("Enter the venue or city."), Length(max=200)],
    )
    package = SelectField("Package", choices=PACKAGE_CHOICES, validators=[Optional()])
    notes = TextAreaField("Anything else?", validators=[Optional(), Length(max=2000)])
    # Honeypot: hidden from people, filled in by bots.
    website = StringField("Website")

    def validate_event_date(self, field):
        if field.data and field.data < date.today():
            raise ValidationError("Choose a date that hasn't passed yet.")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired("Enter your email.")])
    password = PasswordField("Password", validators=[DataRequired("Enter your password.")])
