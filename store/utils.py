from django.core.exceptions import ValidationError

def validate_score(value):
    if not (1.0 <= value <= 5.0):
        raise ValidationError(f"The score must be between 1.0 and 5.0. You provided {value}.")
