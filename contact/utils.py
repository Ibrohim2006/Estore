from django.core.exceptions import ValidationError

def phone_number_validation(phone_number):
    if len(phone_number) == 13 and phone_number[:4] == '+998' and phone_number[1:13].isdigit():
        return True
    raise ValidationError('phone_number is invalid')
