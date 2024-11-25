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


def validate_performance_file(file):
    allowed_extensions = ["csv", "xlsx"]
    ext = file.name.split(".")[-1].lower()
    if ext not in allowed_extensions:
        raise ValidationError("Only CSV or Excel files are allowed.")


unique_school_name = UniqueValidator(
    queryset=School.objects.all(), message="A school with this name already exists."
)
