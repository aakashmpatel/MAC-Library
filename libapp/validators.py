from django.core.exceptions import ValidationError

def validate_pubyr(value):
    if value < 1900 or value > 2016:
        raise ValidationError(u'%s is not a range of 1900 and 2016!' % value)