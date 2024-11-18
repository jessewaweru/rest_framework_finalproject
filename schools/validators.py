from rest_framework.exceptions import ValidationError
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.validators import UniqueValidator
from schools.models import School
import re


def validate_name(value):
    if len(value) < 3 or len(value) > 100:
        raise ValidationError(
            f"Name length must be between 3 and 100 characters. You entered {len(value)} characters."
        )
    return value


def validate_description(value):
    if len(value) < 10:
        raise ValidationError("Description must have at least 10 characters")
    return value


def validate_rating(value):
    if not (0 <= value <= 5):
        raise ValidationError("Rating must be between 0 and 5")
    return value


def validate_website(value):
    url_validator = URLValidator()
    try:
        url_validator(value)
    except DjangoValidationError:
        raise ValidationError("Enter a valid URL for the website")


def validate_contact(value):
    if not re.match(r"^\d{10,15}$", str(value)):
        raise ValidationError("Enter a valid phone number with 10-15 digits.")
    return value


# Validator for awards (list of text)
def validate_award(value):
    if not isinstance(value, list):
        raise ValidationError("Awards must be a list of text entries.")

    if any(not isinstance(award, str) or len(award) == 0 for award in value):
        raise ValidationError("Each award must be a non-empty string.")

    return value


unique_school_name = UniqueValidator(
    queryset=School.objects.all(), message="A school with this name already exists."
)
